""" 
Gets the project codes and returns a tuple for models.py use.
"""

import os
import csv

def get_code_list():

	CODE_BASE_PATH = os.path.dirname(os.path.realpath(__file__))

	# The master file always has to have this name & path unless otherwise specified
	CURRENT_SET_PATH = CODE_BASE_PATH + "/codelist/masterlist.csv"

	try:
		with open(CURRENT_SET_PATH, "rb") as code_file:
			tsv_file = csv.reader(code_file, delimiter="\t")
