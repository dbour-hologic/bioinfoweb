from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from .forms import BiomatcherUploadForm, BiomatcherInputForm
from .models import BiomatcherFileUpload


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

def matcher(request):

	minimum_total_hits = request.POST.get('minimum_total_hits')
	maximum_total_hits = request.POST.get('maximum_total_hits')
	max_mismatches_allowed = request.POST.get('max_mismatches_allowed')
	patterns = request.POST.get('patterns')
	database_selection = request.POST.get('database-selection-hidden')

	q = BiomatcherFileUpload.objects.get(id=database_selection)
	path = q.biomatcher_fileupload
	# Default Storage finds the file directory and can open it
	db_file = default_storage.open(path)

	data = convert_to_fasta(patterns, db_file, max_mismatches_allowed)
	json_data_returned = data.get_json_result()

	return render(request, 'biomatcher/biomatcher_run.html', {'data':json_data_returned})

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
		