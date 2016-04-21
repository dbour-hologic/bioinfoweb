import sys
from sys import argv

import json
import csv
import codecs


# test = [
# 	{
# 		"model":"myapp.articles",
# 		"pk": 1,
# 		"fields": {
# 			"title": "TMA",
# 			"year": 1989,
# 			"citation": "David"
# 		}
# 	},
# 	{
# 		"model":"myapp.articles",
# 		"pk":2,
# 		"fields": {
# 			"title": "INVADER",
# 			"year": 1920,
# 			"citation":"ZIIM"
# 		}
# 	}
# ]

# print test

# {"model":"x", "pk":"#", "fields":{"field":"field"}}

"""
0-1. Name
1-2. Article Title
2-3. Title
3-4. Authors
4-5. Year
5-6. Citation
6-7. Keywords
"""

def file_scanner(filename):

	# Holds all of the file/article objects
	data_list = []

	with open(filename, "r") as data:
		csvfile = csv.reader(data, delimiter="\t")
		for line_number, datapoints in enumerate(csvfile):
			if (line_number==0):
				continue
			data_property = data_factory(	datapoints[0],
											datapoints[1],
											datapoints[3],
											datapoints[4],
											datapoints[5],
											datapoints[6],
											line_number
										)
			data_list.append(data_property)

		return data_list



def data_factory(name, title, author, year, citation, keywords, pk):
	
	MODEL_NAME = "gparchives.Documents"
	PATH_BUILDER = "archives"
	FILE_PATH = PATH_BUILDER + "/" + name

	dict_builder = {}

	field_builder = {}
	field_builder["document"] = FILE_PATH 		# Article File Name (PATH)
	field_builder["title"] = title 						# Article Title
	field_builder["author"] = author 					# Article Authors

	try:
		field_builder["year"] = int(year) 			# Article Year
	except ValueError:
		field_builder["year"] = None

	field_builder["citation"] = citation  		# Article Citation
	field_builder["keywords"] = keywords 			# Article Keywords

	dict_builder["fields"] = field_builder
	dict_builder["model"] = MODEL_NAME
	dict_builder["pk"] = pk


	return dict_builder


def file_writer(dataobjects, saveAs):
	with open(saveAs, "w") as jsonfile:
		json.dump(dataobjects, jsonfile)


if __name__ == "__main__":
	script, filename, saveAs = argv
	create_data = file_scanner(filename)
	finished_data = file_writer(create_data, saveAs)