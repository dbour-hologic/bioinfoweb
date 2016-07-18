from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .forms import BiomatcherUploadForm, BiomatcherInputForm
from .models import BiomatcherFileUpload
import json


def index(request):

	if request.method == "POST":

		print(request.POST)

		upload_form = BiomatcherUploadForm(request.POST, request.FILES)
		input_form = BiomatcherInputForm(request.POST)
		if upload_form.is_valid():
			upload_form.save()
	else:

		input_form = BiomatcherInputForm()
		upload_form = BiomatcherUploadForm()

	return render(request, 'biomatcher/biomatcher.html', {"input_form":input_form, "upload_form":upload_form})

@csrf_exempt
def matcher(request):

	""" Matcher 
		Serves to process the ajax data
	"""

	if request.is_ajax():
		bio_data = json.loads(request.body)
		minimum_total_hits = bio_data['minimum_total_hits']
		maximum_total_hits = bio_data['maximum_total_hits']
		max_mismatches_allowed = bio_data['max_mismatches_allowed']
		patterns = bio_data['patterns']
		database_selection = bio_data['database_selection_hidden']

		q = BiomatcherFileUpload.objects.get(id=database_selection)
		path = q.biomatcher_fileupload
		# Default Storage finds the file directory and can open it
		try:
			db_file = default_storage.open(path)
		except IOError:
			print "No database file found at {0}".format(path)
		data = convert_to_fasta(patterns, db_file, max_mismatches_allowed)
		json_data_returned = data.get_json_result()

	return HttpResponse(json_data_returned, content_type='application/json')
	
def convert_to_fasta(patterns, database_selection, mismatch_score):

	from matcher.pattern_analysis import PatternAnalysis
	from Bio import SeqIO
	from Bio.Seq import Seq
	import tempfile

	temp = tempfile.TemporaryFile()

	lis = patterns.split("\n")
	lis2 = [x +'\n' for x in lis]

	with temp as tmp:
		for lines in lis2:
			tmp.write(lines)
		tmp.seek(0)

		pat = PatternAnalysis()
		pat.run(tmp, database_selection, int(mismatch_score))
		return pat
	return None
		