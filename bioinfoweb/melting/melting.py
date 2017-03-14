# Melting program to send raw bash commands
import os
import subprocess
from bioinfow.settings import common

# From DJANGO
# ----> DJANGO will convert the JSON to string
# ----> STRING is what will be used for this processing

class Query:

	""" Builds a query object from the JSON DATA to be used 
	to create a command line prompt for MELTING 5 """

	def __init__(self, forward, reverse, ionType1, ionConc1, ionType2, ionConc2, oligoConc, hybridType):
		self.forward = forward # 5'-3' Sequence 
		self.reverse = reverse # 3'-5' Sequence 
		self.ionType1 = ionType1 # ion type (Na, Mg, Tris, K) 
		self.ionConc1 = ionConc1 # ion concentration
		self.ionType2 = ionType2 # ion type (Na, Mg, Tris, K)
		self.ionConc2 = ionConc2 # ion concentration 
		self.oligoConc = oligoConc # oligonucleotide concentration
		self.hybridType = hybridType # hybridization type (dnadna, dnarna, etc)
		self.__reverse__()

	# Changes the forward/reverse strand according to the hybrid type chosen
	def __reverse__(self):
		if (self.hybridType == "dnarna"):
			self.reverse = self.reverse.replace("T", "U")
		elif (self.hybridType == "rnadna"):
			self.forward = self.forward.replace("T", "U")
		elif (self.hybridType == "rnarna" or self.hybridType == "mrnarna"):
			self.forward = self.forward.replace("T","U")
			self.reverse = self.reverse.replace("T","U")

def queryBuilder(queryObject):

	""" Constructs the string to be executed on the command prompt """

	q = queryObject

	# Search string that will be executed as a raw command
	queryString = "melting -S %s -C %s -P %s -H %s -E %s=%s:%s=%s" % \
				   (	
				   		q.forward, q.reverse, 
						q.oligoConc, q.hybridType,
						q.ionType1, q.ionConc1,
						q.ionType2, q.ionConc2
				   )

	return queryString
	
def meltingExec(command):

	# Sets up the environmental variable to execute MELTING 5
	base_path = common.PROJECT_ROOT
	melt_path = os.path.join(base_path, "melting5", "MELTING5.1.1", "executable")
	add_path = os.environ['PATH'] + ":" + melt_path

	# Sets up the environmental variable NN_PATH for the melting program
	# The NN_PATH contains the experimental values for MELTING 5
	nn_path = os.path.join(base_path, "melting5", "MELTING5.1.1", "Data")
	os.environ["NN_PATH"] = nn_path

	searchQuery = command
	
	# Sanitary check, remove all possibilities of executing further commands
	searchQuery = searchQuery.replace(";","")

	p = subprocess.Popen(
		searchQuery, 
		stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE, 
		shell=True,
		env=dict(os.environ, PATH=add_path)
	)
	
	#Capture the error message
	stdout, stderr = p.communicate()
	
	# Gets the result log in a dictionary form for parsing
	resultLog = getData(stdout)

	return resultLog

def getData(results):

	""" Used for parsing the error message that is outputted by the Java 
	Melting 5 program. Helps with organizing the data in Jinja afterwards """

	report = {"STATUS":"", "ENTHALPY":"", 
				"ENTROPY":"", "TM":"", 
					"MESSAGE":""}

	listOf = results.split("\n") # Breaks down the output for parsing
	isThere = searchResults(listOf) # Check if there are results present

	# If results are present, parse out results into a dictionary
	if (isThere):

		# Check if the results contain a warning
		if listOf[0] != "":
			report["STATUS"] = listOf[0]
			report["MESSAGE"] = listOf[1]
		else:
			report["STATUS"] = listOf[0]
			report["MESSAGE"] = ""

		for pos, x in enumerate(listOf):
			if (x.find("Enthalpy") != -1):
				report["ENTHALPY"] = x
			elif (x.find("Entropy") != -1):
				report["ENTROPY"] = x
			elif (x.find("degrees") != -1):
				report["TM"] = x

	else:

		severePos = 0 # Holds the position of the "severe" error
		warningPos = 0 # Holds the position of the "warning" error
		counts = 0 # Checks to see if it has both errors and parses respectively

		for pos, x in enumerate(listOf):

			if (x.find("SEVERE") != -1):
				counts += 1
				severePos = pos
			elif (x.find("WARNING") != -1):
				counts += 1
				warningPos = pos

		# Parses only severe error if it has one error
		if (counts < 2):
			report["STATUS"] = listOf[severePos]
			report["MESSAGE"] = listOf[severePos+1]
		# Parses only warning error if it has both errors (More informative)
		else:
			report["STATUS"] = listOf[warningPos]
			report["MESSAGE"] = listOf[warningPos+1]

	return report

def searchResults(datalist):

	""" Function to check if melting data is available """

	for pos, x in enumerate(datalist):
		if (x.find("Enthalpy") != -1):
			return True
	return False 
		
