import os
import datetime
import json
import mimetypes

from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.uploadedfile import UploadedFile
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import PqAttachment, PqResults, Worklist, CombineResults
from .forms import WorklistInputForm

from rcall.rcaller import R_Caller


def create_timestamp():
	""" Creates the timestamp """
	return ('{:%Y%m%d-%H-%M-%S}'.format(datetime.datetime.now()))

def add_attachment(request):
	if request.method == "POST":
		analysis_id = request.POST['analysis_id']
		worklist_options = request.POST.get('file_upload_selection', False)
		stats_options = request.POST.get('stats-option', "None")
		limit_options = request.POST.getlist('limit-options')[0]
		assay_options = request.POST.getlist('assay-analysis')[0]
		graph_options = request.POST.getlist('graph-options')[0]
		combine_options = request.POST.get('combine-file')
		submitter = request.POST['submitter']
		files = request.FILES.getlist('file[]')

		format_analysis_id = analysis_id + create_timestamp()

		for a_file in files:

			instance = PqAttachment(
				analysis_id = format_analysis_id,
				file_name = a_file.name,
				attachment= a_file,
				submitter= submitter
			)

			instance.save()

		if combine_options:

			return create_and_serve_combined_file(request, format_analysis_id)



		return add_attachment_done(request, submitter, stats_options, assay_options, format_analysis_id, worklist_options, limit_options, graph_options)
	
	# Have to find a better methd for this one later
	try:
		worklist_template = Worklist.objects.get(filename="paraflu-default-worklist.csv")
	except ObjectDoesNotExist:
		worklist_template = None

	worklist_form = WorklistInputForm();

	return render(request, "pqanalysis/pqanalysis.html", {"worklist_form":worklist_form, "worklist_template":worklist_template})



def create_and_serve_combined_file(request, format_analysis_id):

	""" Gets combined file data and serves """

	from .fcombiner import FusionCombiner
	import shutil
	import pandas

	query_db = PqAttachment.objects.filter(analysis_id__exact = format_analysis_id)
	files_dir = os.path.join(settings.MEDIA_ROOT, "/".join(query_db.values()[0]['attachment'].split("/")[:-1]))

	SAVE_DATA_DIR = os.path.join(settings.MEDIA_ROOT, 'pqcombined')
	list_of_files = [os.path.join(files_dir, files) for files in os.listdir(files_dir)]
	f = FusionCombiner(list_of_files, "P 1/2/3/4")

	if not isinstance(f.mega_combination, pandas.core.frame.DataFrame):
		error_msg = "The files provided could not be combined. Please check if they are from the same run. If you believe this message is not correct, please consult one of the contacts."
		worklist_form = WorklistInputForm();
		# Have to find a better methd for this one later
		try:
			worklist_template = Worklist.objects.get(filename="paraflu-default-worklist.csv")
		except ObjectDoesNotExist:
			worklist_template = None
		worklist_form = WorklistInputForm();
		return render(request, "pqanalysis/pqanalysis.html", {"error_msg":error_msg, "worklist_form":worklist_form, "worklist_template":worklist_template})

	data_save = os.path.join(SAVE_DATA_DIR, format_analysis_id + "_combined.xlsx")
	f.write_combined_multiple(data_save)

	combined_model = CombineResults()
	combined_model.combine_file_name = format_analysis_id + "_combined.xlsx"
	combined_model.combine_file_dir = os.path.join("pqcombined", format_analysis_id + "_combined.xlsx")
	combined_model.save()

	fsock = open(os.path.join(data_save), "rb")
	response = HttpResponse(fsock, content_type="text/xlsx")
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(format_analysis_id + "_combined.xlsx")

	return response

def add_attachment_done(request, user_name, stats_options, assay, format_analysis_id, worklist_options, limit_options, graph_options):
	""" 
		(1) Append analysis_id to R markdown output.
		(2) Execute necessary programs
		(3) Go to results page
	"""

	logs = ""

	query_db = PqAttachment.objects.filter(analysis_id__exact = format_analysis_id)
	files_dir = os.path.join(settings.MEDIA_ROOT, "/".join(query_db.values()[0]['attachment'].split("/")[:-1]))

	if assay == 'Paraflu':

		r = R_Caller(user_name, stats_options, 'Paraflu', files_dir, format_analysis_id, graph_options)

		worklist_query = Worklist.objects.get(id=worklist_options)
		worklist_filename = str(worklist_query.filename)
		worklist_path = os.path.join(settings.MEDIA_ROOT, str(worklist_query.file))

		DEFAULT_LIMIT_OPTION = os.path.join(settings.MEDIA_ROOT, "limits/assay.limits.csv")

		# Arg 'limit_options' is not used for now, but DEFAULT will be used.
		logs = r.execute(default=False, user_name=user_name, data_dir=files_dir, stats_option=stats_options, assay_type='Paraflu', 
						 analysis_id=format_analysis_id, wrk_list=worklist_path, limits_list=DEFAULT_LIMIT_OPTION, graphing_type=graph_options)

	log_str = ""

	run_completed = True

	while True:

	    line = logs.stdout.readline()
	    log_str += line + "\n"

	    if "Execution halted" in line:
	        print("FOUND AN ERROR!.")
	        run_completed = False
	        break

	    if line == '':
	        break

	if not run_completed:
		return render(request, "pqanalysis/pqerror.html", {"error_out":log_str})

	program_timed_out = shuttle_dir('paraflu')

	return view_results(request)

def shuttle_dir(assay_location):
	""" Shuttles and saves the output """

	import time
	import shutil

	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	GET_DATA = os.path.join(BASE_DIR, 'rcall', 'pqresults', assay_location)
	SAVE_DATA = os.path.join(settings.MEDIA_ROOT, 'pqresults', 'results')

	que = []

	# This is a hack, may need to find a way to optimize this
	# It's to wait for the R script to finally finish

	timed_out = True

	# Maximum waiting time of 480 seconds before timing out.
	for counts in range(480):

		for results in os.listdir(GET_DATA):
			if results.endswith('.html'):
				que.append(results)

		if len(que) <= 0:
			time.sleep(1)
		else:
			timed_out = False
			break
	
	if not timed_out:
		for pq_files in que:
			# (1) Here's where you look up the file and save to database
			pq = PqAttachment.objects.filter(analysis_id__exact = pq_files.replace(".html",""))
			try:
				pq[0].pqresults_set.create(pq_file_name=pq_files, file_dir=os.path.join(GET_DATA, pq_files))
				# (2) Here's where you move the file
			except IndexError:
				print("PQReportCompiler2.html default is in the same folder where shuttling occurs. Please remove.")
			try:
				shutil.move(os.path.join(GET_DATA, pq_files), SAVE_DATA)
			except IOError:
				print("File has already moved.")

	return timed_out

def view_results(request):

	SAVE_DATA = os.path.join(settings.MEDIA_ROOT, 'pqresults', 'results')

	file_dict = {}

	for files in os.listdir(SAVE_DATA):
		if files.endswith('.html'):
			try:
				query_result = PqAttachment.objects.filter(analysis_id__exact = files.replace(".html",""))
				file_dict[files] = {"attachment":query_result[0],"html_dir":os.path.join('pqresults','results',files)}
			except IndexError:
				# Have to create a fake object here to resemble above result for templating reasons
				file_dict[files] = {"No data found"}
				print("No such file found.")

	return render(request, 'pqanalysis/pqresults.html', {'file_dict':file_dict})

@csrf_exempt
def get_worklist_update(request):


	if request.method == 'GET':
		worklist_list = Worklist.objects.all()
		work_list_all = []
		for element in worklist_list.values():
			work_list_all.append(
									{'id':element['id'], 
									'filename':element['filename']}
								)

		return HttpResponse(json.dumps(work_list_all), content_type='application/json')

@csrf_exempt
def worklist_upload(request):
	""" Worklist uploader - using ajax to allow
	users to custom upload their database
	"""

	if request.method == 'POST':
		file = request.FILES['file']
		wrapped_file = UploadedFile(file)
		filename = wrapped_file.name
		file_size = wrapped_file.file.size

		# Manual writing file object since forms not necessary
		file_obj = Worklist()
		file_obj.filename = str(filename)
		file_obj.file = file
		file_obj.save()

		file_url = "uploaded_data/"
		file_delete_url = reverse('upload-delete', args=[file_obj.pk])

		# Generate JSON Response
		response = []
		response.append({
			"name": filename,
			"size": file_size,
			"url": file_url,
			"delete_url": file_delete_url,
			"delete_type:":"POST",
		})
		response_data = json.dumps(response)

		# Check for JSON Data Type
		if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
			mimetype = 'application/json'
		else:
			mimetype = 'text/plain'
		return HttpResponse(response_data, content_type=mimetype)
	else:
		return HttpResponse('Only POST Accepted')

@csrf_exempt
def worklist_delete(request, pk):
	""" View for deleting via AJAX """
	if request.method == 'POST':
		file = get_object_or_404(Worklist, pk=pk)
		file.delete()
		return HttpResponse(str(pk))
	else:
		return HttpResponseBadRequest("Only POST Accepted")

@csrf_exempt
def ajax_uploaded_worklist(request):

	import csv

	if request.is_ajax():

		worklist_response_data = json.loads(request.body)

		media_path = os.path.join(settings.MEDIA_ROOT, "worklist")
		worklist_name = worklist_response_data['json']['worklist_name']
		submission_name = worklist_response_data['json']['submitter_name']

		file_name_generator = worklist_name + create_timestamp() + ".csv"
		file_save_path = os.path.join(media_path, file_name_generator)

		with open(file_save_path, "wb") as worklist_file:
			csv_writer = csv.writer(worklist_file, delimiter=",")

			for key, value in worklist_response_data['json'].iteritems():
				if key == "worklist_name" or key == "submitter_name":
					continue
				else:

					# Temporary storage to parse the JSON data into a predictable format
					temp_data_storage = {
						"name":"",
						"type":"",
						"category":"",
					}

					for category, data_value in value.iteritems():
						parse_value = category.split(".")[1]
						temp_data_storage[parse_value] = data_value

					line_to_write = [temp_data_storage["name"], temp_data_storage["type"], temp_data_storage["category"]]
					csv_writer.writerow(line_to_write)

			worklist_save_file = Worklist()
			worklist_save_file.filename = str(worklist_name)
			worklist_save_file.file = file_save_path
			worklist_save_file.save()


	return HttpResponse("success")