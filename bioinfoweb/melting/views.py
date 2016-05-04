from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import MeltForm
from .melting import *
import json, subprocess


# Create your views here.

def ajaxtest(request):

	meltform = MeltForm(auto_id=False)
	return render(request, 'melt.html', {'meltform':meltform})

@csrf_exempt
def ajaxresponse(request):

	koArray = request.POST.get('koArray') # Retrieves the knockout array for comp bases
	koArrayLoad = json.loads(koArray)
	properties = request.POST.get('propertiesArray') # Retrieves the salts/types
	propertiesLoad = json.loads(properties)

	queryObj = sequenceCreator(koArrayLoad, propertiesLoad) # Creates the query object which has all necessary information for melting cmd prompt
	s = queryBuilder(queryObj)
	results = meltingExec(s)
	json_response = {'finalData':{'results':results}}

	return HttpResponse(json.dumps(json_response), content_type='application/json')

## Method to convert the JSON data into proper nucleotide sequences with its melting conditions
# @param jsondata is the data received from melting sequence form
# @return query object with all of the properties of the search and its environment
def sequenceCreator(jsonDataKo, jsonDataProp):

	senseStrand = "" # Used building final sequence of 5'-3' (Unmodifiable)
	antisenseStrand = "" # Used building final sequence of 3'-5' (Modifiable)

	senseDict = jsonDataKo.get('seqArray') # Returns a list of dictionary with sequence properties of 5'-3'
	antisenseDict = jsonDataKo.get('comArray') # Returns a list of dictionary with sequence properties of 3'-5'

	for x in range(len(senseDict)):

		senseStrand += senseDict[x].get('originalBase')
		antisenseStrand += antisenseDict[x].get('compBase')

	meltEnv = jsonDataProp.get('attributes')
	# Gets the values of [0]oligo concentration, [1]hybridization type, [2]Na+, [3]Mg++ in that order
	meltArr = [str(meltEnv[z].get('value')) for z in range(len(meltEnv))]
	meltArr[0] = str(float(meltArr[0])/1000000) # conversion of uM to m
	meltArr[2] = str(float(meltArr[2])/1000) # conversion of mM to M
	meltArr[3] = str(float(meltArr[3])/1000) # conversion of mM to M
	

	# Create query object to send to the command line
	queryObj = Query(senseStrand, antisenseStrand, "Na", meltArr[2], "Mg", meltArr[3], meltArr[0], meltArr[1])
	return queryObj

	