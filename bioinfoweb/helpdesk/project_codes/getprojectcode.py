""" 
Gets the project codes and returns a tuple for models.py use.
"""

import os
import csv

def get_code_list():

	CODE_BASE_PATH = os.path.dirname(os.path.realpath(__file__))

	# The master file always has to have this name & path unless otherwise specified
	CURRENT_SET_PATH = CODE_BASE_PATH + "/codelist/masterlist.tsv"

	# Tuple to return
	project_code_list = ()

	try:
		with open(CURRENT_SET_PATH, "rb") as code_file:
			tsv_file = csv.reader(code_file, delimiter="\t")
			# Data structure (string, (string)), ...
			for itemcode in tsv_file:

				itemcode_concat = itemcode[0] + " " + itemcode[1]
				build_project_tuple = (itemcode_concat, itemcode_concat)
				project_tuple_data = ((build_project_tuple),)
				project_code_list += project_tuple_data

	except IOError as err:
		print "I/O error({0}): {1}".format(err.errno, err.strerror)
		print "Could not find project code list file."

	# print project_code_list

	return project_code_list
