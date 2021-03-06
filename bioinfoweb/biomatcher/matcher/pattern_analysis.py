""" Pattern Analysis Program
Author: David Bour
Date: 2016-06-28

"""

from Bio import SeqIO
from Bio.Seq import Seq
from matching_lib import dna_match_all
import json

class RunIdentifier(object):

	""" 
	The RunIdentifier class is used to group the results of 
	hits to a specific pattern; a one to one relationship. 
	"""

	def __init__(self, id, subject, pattern, pattern_id, hit_locations, total_hits, mismatch_tolerance_set):

		""" Constructor for RunIdentifier

		Args:
			id - the FASTA parsed ID of the subject (str)
			subject - the sequence to be queried (str)
			pattern - the pattern to be queried against the subject (str)
			pattern_id - the FASTA parsed ID of the pattern (str)
			hit_locations - all starting positions of matches (list)
			total_hits - total number of times the specific pattern hit per sequence (int)
			mismatch_tolerance_set - the mismatch tolerance set for this particular run

		"""

		self.id = id
		self.subject = subject
		self.pattern = pattern
		self.pattern_id = pattern_id
		self.hit_locations = hit_locations
		self.total_hits = total_hits
		self.mismatch_tolerance_set = mismatch_tolerance_set

	def get_coordinates(self):
		"""
		Generates a list with coordinates for the start position
		and end position of each pattern match. This is the actual
		positions relative to the subject, not the python indexes
		used for slicing.

		Returns:
			list of coordinate tuples (<start>:<end>)
		"""

		locations = []
		for location in self.hit_locations:
			# Actual Start (Not Python Slice Indexing)
			start_location = location + 1 
			# Actual End (Not Python Slice Indexing)
			end_location = location + len(self.pattern)

			locations.append((start_location, end_location))

		return locations

	def get_partial_sequences(self):
		"""
		Generates a list of partial sequences from the 
		coordinate data.

		Returns:
			dict of subject sequences where pattern has made a match (dict) (int tuple)
		"""

		# <Key> sequence | <Value> coordinate position to obtain sequence
		partial_sequences = {}

		for coords in self.get_coordinates():
			# Note, start position had -1 since python indexing starts at 0
			start_position = coords[0] - 1
			end_position = coords[1]
			sub_seq = self.subject[start_position:end_position]

			# Python indexing starts at 0, but we want to display actual for results.

			if partial_sequences.get(sub_seq) == None:
				partial_sequences[sub_seq] = [coords]
			else:
				partial_sequences[sub_seq].append([coords])
		return partial_sequences


	def print_friendly(self):

		print "PATTERN ID: {0}".format(self.pattern_id)
		print "PATTERN SEQ: {0}".format(self.pattern)
		print "QUERY_ID: {0}".format(self.id)
		print "Mismatch tolerance has been set to {0}\n".format(self.mismatch_tolerance_set)

		for location in self.hit_locations:
			end_point = len(self.pattern) + location - 1
			print "Pattern: {0}".format(self.pattern)
			print "Subject: {0}".format(self.subject[location:end_point+1])
			print "Subj Start: {0} Subj End: {1}".format(location+1, end_point)
			print "\n"


class PatternAnalysis(object):

	""" Main Analysis Component

	Makes use of Biopython as the FASTA parser and a custom DNA matching
	library for pattern matching.

	"""

	def __init__(self):
		"""
		Constructor for Pattern Analysis Program

		list_of_queries (dict) - Holds a unique sequence ID (key) along with a list
		of RunIdentifier objects (value). Helps to keep all of the queries against
		the subjects.

		loaded_patterns (list) - Holds all of the patterns in a SeqRecord object format

		loaded_subjects (list) - Holds all of the target sequences in a SeqRecord object format

		"""
		self.list_of_queries = {}
		self.loaded_patterns = []
		self.loaded_subjects = []

	def _load_patterns(self, pattern_file):
		"""
		Reads a .txt file to load patterns to query against
		the subjects. Uses Biopython module for FASTA parsing.

		Args:
			pattern_file - directory path to pattern file (str)
		Returns:
			true if there were any patterns available, false if not (bool)

		"""

		try:
			for pat_records in SeqIO.parse(pattern_file, "fasta"):
				self.loaded_patterns.append(pat_records)
		except IOError:
			print "Failed to find pattern file at '{0}'".format(pattern_file)

		return len(self.loaded_patterns) != 0

	def _load_subjects(self, subject_file):
		"""
		Reads a .txt file to load subject sequences to query against
		the patterns. Uses Biopython module for FASTA parsing.

		Args:
			subject_file - directory path to pattern file (str)

		"""
		try:
			for records in SeqIO.parse(subject_file, "fasta"):
				self.loaded_subjects.append(records)
		except IOError:
			print "Failed to find subject file at '{0}'".format(subject_file)

	def run(self, pattern_file, subject_file, mismatch_tolerance=0):
		"""
		CORE LOGIC OF PROGRAM
		> Sets up the environment and runs the program.

		Args
			pattern_file - file path of the pattern file in FASTA <*.fasta> format (str)
			subject_file - file path of the subject file in FASTA <*.fasta> format (str)
			mismatch_tolerance - the amount of mismatches to tolerate (int)
		Returns
			true/false - if the run was successful (bool)
		"""

		# Load up the data from the files
		pattern_available = self._load_patterns(pattern_file)

		# End execution prematurely if there's no patterns
		if not pattern_available:
			return False

		self._load_subjects(subject_file)

		# Run each subject against a set of oligonucleotide patterns
		for num, subject in enumerate(self.loaded_subjects):

			# The sequence ID
			run_id = subject.id
			# The sequence itself
			run_seq = str(subject.seq).rstrip()
			# Create a placeholder to hold all patterns searched against this
			# particular sequence.
			self.list_of_queries[run_id] = []

			for pattern in self.loaded_patterns:
				# The pattern ID
				pattern_id = pattern.description
				# The pattern sequence
				pattern_seq = str(pattern.seq).rstrip()
				# Core matching algorithm
				results = dna_match_all(pattern_seq, run_seq, mismatch_tolerance)
				# Create the sequence-pattern pair object to store
				run_create = RunIdentifier(
											run_id, 
											run_seq, 
											pattern_seq, 
											pattern_id, 
											results, 
											len(results), 
											mismatch_tolerance
										  )
										
				self.list_of_queries[run_id].append(run_create)
		return True

	def size(self):
		return len(self.list_of_queries)

	def filter_by_frequency(self, minCut=0, maxCut=0):

		"""
		Filters the list of results by the chosen number of total
		matches a pattern has made to a specific subject. 

		Example: If pattern ATCG matched two times to a single subject,
		and the max number of hits allowed is 1, the pattern will be 
		completely dropped from the hit results. If it was set to a minimum
		of two matches, it will pass.

		Args:
			minCut - the minimum number of times a pattern has to match a single subject
			maxCut - the maximum number of times a pattern can match to a single subject

		"""

		for subject, run_id in self.list_of_queries.iteritems():

			for run in run_id[:]:
				if run.total_hits < minCut:
					run_id.remove(run)
				if run.total_hits > maxCut:
					run_id.remove(run)


	def print_features(self):

		""" Prints results to terminal """
		for key, value in self.list_of_queries.iteritems():
			for items in value:
				items.print_friendly()
				print items.get_coordinates()
				print "##### ----- #####\n"

	def get_json_result(self):

		"""
		JSON data for web use


		Visual Blueprint

		[	<json_results>
			{	<subject_list>
				[	<pattern_list>
					{	
						<pattern 1 (json_builder)>
					},
					{
						<pattern 2 (json_builder)>
					},
					{
						<pattern 3 (json_builder)>
					}
				]
			},
			{
				<subject_list>
				[	<pattern_list>
					{
						<pattern 1 (json_builder)>
					},
					{
						<pattern 2 (json_builder)>
					}
				]
			},
		]

		"""

		# Holds the JSON objects 
		json_results = []

		for subject, run_id in self.list_of_queries.iteritems():

			# Holds the assortment of targets
			subject_list = {}

			# Holds the assortment of patterns per one subject
			pattern_list = []

			for run in run_id: # All of the RunIdentifier Objects | Different patterns

				json_obj = self._json_builder(run)
				pattern_list.append(json_obj)
			
			subject_list[subject] = pattern_list
			json_results.append(subject_list)

		return json.dumps(json_results)
	
	def _json_builder(self, run_id):

		"""
		The json_builder builds only from one 'pattern'.

		Args:
			run_id - a RunIdentifier object that contains one pattern <RunIdentifier>
		Returns:
			a dictionary object containing one pattern and its attributes <dict>


		#### #### #### #### ####
		Visual Blueprint of Object
		#### #### #### #### ####

		---------------------- Generic Example
		{ <dict builder> 
			{
				<field builder>
			}
		}
		---------------------- Specific Example
		{ 
			"Pattern 1" : { 
							"subject_id" : subject name <str>,
							"pattern_sequence" : pattern seq <str>, 
							"subj_sequence" : subject seq <str>,
							"tolerance" : mismatch tolerance used <int>,
							"sub_seq" : sub-sequences obtained from hit list as well as their coords <dict>,
							"hit_coordinates" : a list of start to end coordinates of each hit <list>
							"total_hits" : total amount of times a pattern hit a sequence
						  }
		}


		"""

		dict_builder = {}

		field_builder = {}
		
		field_builder["subject_id"] = run_id.id
		field_builder["pattern_sequence"] = run_id.pattern
		field_builder["subj_sequence"] = run_id.subject
		field_builder["tolerance"] = run_id.mismatch_tolerance_set
		field_builder["sub_sequences"] = run_id.get_partial_sequences()
		field_builder["hit_coordinates"] = run_id.get_coordinates()
		field_builder["total_hits"] = run_id.total_hits

		dict_builder[run_id.pattern_id] = field_builder

		return dict_builder

if __name__ == '__main__':

	test_run = PatternAnalysis()
	test_run.run('data/testlacto.fasta', 'data/probes.fasta', 0)
	print test_run.print_friendly()




