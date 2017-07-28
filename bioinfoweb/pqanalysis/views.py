import os
import datetime
import json

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.uploadedfile import UploadedFile
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import PqAttachment, Worklist, CombineResults, Limits, RunRecovery
from .forms import WorklistInputForm, LimitsInputForm, RunRecoveryForm

from rcall.rcaller import R_Caller, R_Caller_TMA


def create_timestamp():
    """ Creates the timestamp """
    return ('{:%Y%m%d-%H-%M-%S}'.format(datetime.datetime.now()))


def add_attachment(request):
    """
    add_attachment is the main entry point of the program. A user
    may POST or GET the page for the pqanalysis to take place.
    """
    if request.method == "POST":

        get_assay_type = request.POST.get('assay-option-selection')

        analysis_id = request.POST.get('analysis_id')
        submitter = request.POST.get('submitter')
        files = request.FILES.getlist('file[]')

        # Create a unique_id to tie the files uploaded to a unique group identifier
        format_analysis_id = analysis_id + create_timestamp()

        for a_file in files:
          instance = PqAttachment(
            analysis_id=format_analysis_id,
            file_name=a_file.name,
            attachment=a_file,
            submitter=submitter
          )

          instance.save()

        if get_assay_type == 'fusion':

            worklist_options = request.POST.get('file_upload_selection', False)
            stats_options = request.POST.get('stats-option', "None")
            limit_options = request.POST.get('file_limits_upload_selection', False)
            assay_options = request.POST.getlist('assay-analysis')[0]
            graph_options = request.POST.getlist('graph-options')[0]
            ignoreflag_options = request.POST.getlist('ignoreflags')
            combine_options = request.POST.get('combine-file')

            if combine_options:
                return create_and_serve_combined_file(request, format_analysis_id)

            if ignoreflag_options:
                ignoreflag_options = "TRUE"
            else:
                ignoreflag_options = "FALSE"

            return add_attachment_done(request,
                                       submitter,
                                       stats_options,
                                       assay_options,
                                       format_analysis_id,
                                       worklist_options,
                                       limit_options,
                                       graph_options,
                                       ignoreflag_options)
        else:

            worklist_options = request.POST.get('file_upload_selection_tma')
            limit_options = request.POST.get('file_limits_upload_selection_tma')
            recovery_options = request.POST.get('file_upload_selection_recovery')
            assay_options = request.POST.getlist('assay-analysis')[0]

            return add_attachment_done_tma(
              request,
              submitter,
              format_analysis_id,
              assay_options,
              worklist_options,
              limit_options,
              recovery_options
            )

    worklist_form = WorklistInputForm();
    limits_form = LimitsInputForm();
    recovery_form = RunRecoveryForm();

    return render(request, "pqanalysis/pqanalysis.html", {"worklist_form": worklist_form,
                                                          "limits_form": limits_form,
                                                          "recovery_form": recovery_form})


def create_and_serve_combined_file(request, format_analysis_id):
    """ Gets combined file data and serves
    Function is currently not compatible with
    AMR/FLU.
    """

    from .fcombiner import FusionCombiner
    import pandas

    query_db = PqAttachment.objects.filter(analysis_id__exact=format_analysis_id)
    files_dir = os.path.join(settings.MEDIA_ROOT, "/".join(query_db.values()[0]['attachment'].split("/")[:-1]))

    SAVE_DATA_DIR = os.path.join(settings.MEDIA_ROOT, 'pqcombined')
    list_of_files = [os.path.join(files_dir, files) for files in os.listdir(files_dir)]
    f = FusionCombiner(list_of_files, "P 1/2/3/4")

    if not isinstance(f.mega_combination, pandas.core.frame.DataFrame):

      error_msg = "The files provided could not be combined.   \
            Please check if they are from the same run.  \
            If you believe this message is not correct,  \
            please consult one of the contacts."

      # Have to find a better methd for this one later
      try:
        worklist_template = Worklist.objects.get(filename="paraflu-default-worklist.csv")
      except ObjectDoesNotExist:
        worklist_template = None

      worklist_form = WorklistInputForm()
      limits_form = LimitsInputForm()
      recovery_form = RunRecoveryForm()

      return render(request, "pqanalysis/pqanalysis.html", {"error_msg": error_msg,
                                                            "worklist_form": worklist_form,
                                                            "worklist_template": worklist_template,
                                                            "limits_form": limits_form,
                                                            "recovery_form": recovery_form})

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


# Used for TMA Only
def add_attachment_done_tma(
  request,
  user_name,
  format_analysis_id,
  assay_option,
  worklist_file,
  limits_file,
  recovery_file
):
    query_db = PqAttachment.objects.filter(analysis_id__iexact=format_analysis_id)
    files_dir = os.path.join(settings.MEDIA_ROOT, "/".join(query_db.values()[0]['attachment'].split("/")[:-1]))

    worklist_query = Worklist.objects.get(id=worklist_file)
    worklist_path = os.path.join(settings.MEDIA_ROOT, str(worklist_query.file))
    limits_query = Limits.objects.get(id=limits_file)
    limits_path = os.path.join(settings.MEDIA_ROOT, str(limits_query.file))
    recovery_query = RunRecovery.objects.get(id=recovery_file)
    recovery_path = os.path.join(settings.MEDIA_ROOT, str(recovery_query.file))

    r = R_Caller_TMA(user_name, assay_option, format_analysis_id, files_dir, worklist_path, limits_path, recovery_path)
    logs = r.execute()

    log_str = ""
    run_completed = True


    while True:
      line = logs.stdout.readline()
      log_str += line + "\n"

      if "Execution halted" in line:
        print("Found an error.")
        run_completed = False
        break
      if line == '':
        break

    if not run_completed:
      return render(request, "pqanalysis/pqerror.html", {"error_out": log_str})

    return view_results(request)


# Used for Fusion Only
def add_attachment_done(request,
                        user_name,
                        stats_options,
                        assay,
                        format_analysis_id,
                        worklist_options,
                        limit_options,
                        graph_options,
                        ignoreflag_options):
    """
        (1) Append analysis_id to R markdown output.
        (2) Execute necessary programs
        (3) Go to results page
    """

    logs = ""

    query_db = PqAttachment.objects.filter(analysis_id__exact=format_analysis_id)
    files_dir = os.path.join(settings.MEDIA_ROOT, "/".join(query_db.values()[0]['attachment'].split("/")[:-1]))

    r = R_Caller(user_name, stats_options, assay, files_dir, format_analysis_id, graph_options)

    worklist_query = Worklist.objects.get(id=worklist_options)
    worklist_path = os.path.join(settings.MEDIA_ROOT, str(worklist_query.file))

    limitslist_query = Limits.objects.get(id=limit_options)
    limitslist_path = os.path.join(settings.MEDIA_ROOT, str(limitslist_query.file))

    logs = r.execute(default=False,
                     user_name=user_name,
                     data_dir=files_dir,
                     stats_option=stats_options,
                     assay_type=assay,
                     analysis_id=format_analysis_id,
                     wrk_list=worklist_path,
                     limits_list=limitslist_path,
                     graphing_type=graph_options,
                     ignoreflags_options=ignoreflag_options)

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
      return render(request, "pqanalysis/pqerror.html", {"error_out": log_str})

    # program_timed_out = shuttle_dir('rscripts')

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
      pq = PqAttachment.objects.filter(analysis_id__exact=pq_files.replace(".html", ""))
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
        query_result = PqAttachment.objects.filter(analysis_id__exact=files.replace(".html", ""))
        file_dict[files] = {"attachment": query_result[0],
                            "html_dir": os.path.join('pqresults', 'results', files)}
      except IndexError:
        # Have to create a fake object here to resemble above result for templating reasons
        file_dict[files] = {"No data found"}
        print("No such file found.")

  return render(request, 'pqanalysis/pqresults.html', {'file_dict': file_dict})


@csrf_exempt
def get_worklist_update(request):
  if request.method == 'GET':
    worklist_list = Worklist.objects.all()
    work_list_all = []
    for element in worklist_list.values():
      work_list_all.append(
        {'id': element['id'],
         'filename': element['filename'],
         'filetype': element['worklist_type']}
      )

    return HttpResponse(json.dumps(work_list_all), content_type='application/json')


@csrf_exempt
def get_recovery_update(request):
  if request.method == 'GET':
    recovery_list = RunRecovery.objects.all()
    recovery_list_all = []
    for element in recovery_list.values():
      recovery_list_all.append(
        {
          'id': element['id'],
          'filename': element['filename']
        }
      )
  return HttpResponse(json.dumps(recovery_list_all), content_type='application/json')


@csrf_exempt
def get_limitslist_update(request):
  if request.method == 'GET':
    limits_list = Limits.objects.all()
    limits_list_all = []
    for element in limits_list.values():
      limits_list_all.append(
        {
         'id': element['id'],
         'filename': element['filename'],
         'filetype': element['limits_type']
        }
      )

  return HttpResponse(json.dumps(limits_list_all), content_type='application/json')


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
      "delete_type:": "POST",
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


def worklist_get(request, pk):
  import csv

  # Returns a representation of the file
  json_return = {"header": [], "rows": []}

  if request.method == 'GET':

    file = get_object_or_404(Worklist, pk=pk)

    media_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
    with open(media_path) as f:
      csv_reader = csv.reader(f, delimiter=",")
      for num, lines in enumerate(csv_reader):
        if num == 0:
          json_return["header"].append({
            "term": "term",
            "type": "type",
            "logvector": "logvector"
          })
        else:
          json_return["rows"].append({
            "term": lines[0],
            "type": lines[1],
            "logvector": lines[2],
          })

    to_json = json.dumps(json_return)

    mimetype = "text/plain"

    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
      mimetype = "application/json"

    return HttpResponse(to_json, content_type=mimetype)
  else:
    return HttpResponse("Only GET Requests Allowed.")


@csrf_exempt
def worklist_delete(request, pk):
  """ View for deleting via AJAX """
  if request.method == 'POST':
    file = get_object_or_404(Worklist, pk=pk)
    file.delete()
    return HttpResponse(str(pk))
  else:
    return HttpResponseBadRequest("Only POST Accepted")


def limitslist_get(request, pk):
  import csv

  json_return = {"header": [], "rows": []}

  if request.method == 'GET':

    file = get_object_or_404(Limits, pk=pk)

    media_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
    with open(media_path) as f:
      csv_reader = csv.reader(f, delimiter=",")
      for num, lines in enumerate(csv_reader):

        if num == 0:
          json_return["header"].append({
            "sampletype": "sampletype",
            "channel": "channel",
            "threshold": "threshold",
            "direction": "direction",
          })
        else:

          json_return["rows"].append({
            "sampletype": lines[0],
            "channel": lines[1],
            "threshold": lines[2],
            "direction": lines[3]
          })

    to_json = json.dumps(json_return)
    mimetype = "text/plain"

    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
      mimetype = "application/json"

    return HttpResponse(to_json, content_type=mimetype)
  else:
    return HttpResponse("Only GET Requests Allowed")


@csrf_exempt
def ajax_uploaded_limits(request, type_of):
  import csv

  if request.is_ajax():

    limits_response_data = json.loads(request.body)

    media_path = os.path.join(settings.MEDIA_ROOT, "limits")
    limitslist_name = limits_response_data['json']['limitslist_name']
    submission_name = limits_response_data['json']['submitter_name']

    file_name_generator = limitslist_name + create_timestamp() + ".csv"
    file_save_path = os.path.join(media_path, file_name_generator)

    with open(file_save_path, "wb") as limitslist_file:

      limits_headers = ["sample.type", "Channel", "threshold", "direction"]

      if type_of == 'tma':
        limits_headers = ["SampleType", "Interpretation.2_min", "Interpretation.2_max", "GIC.TT_max"]

      csv_writer = csv.writer(limitslist_file, delimiter=",")

      csv_writer.writerow(limits_headers)

      for key, value in limits_response_data['json'].iteritems():
        if key == "limitslist_name" or key == "submitter_name":
          continue
        else:


          if type_of == 'fusion':

            # Temporary storage to parse the JSON data into a predictable format
            temp_data_storage = {
              "name": "",
              "channel": "",
              "threshold": "",
              "logic": ""
            }

            for category, data_value in value.iteritems():
              parse_value = category.split(".")[1]
              temp_data_storage[parse_value] = data_value

            line_to_write = [temp_data_storage["name"],
                             temp_data_storage["channel"],
                             temp_data_storage["threshold"],
                             temp_data_storage["logic"]]

            csv_writer.writerow(line_to_write)

          else:

            # Temporary storage to parse the JSON data into a predictable format
            temp_data_storage_tma = {
              "name": "",
              "minthreshold": "",
              "maxthreshold": "",
              "icthreshold": ""
            }

            for category, data_value in value.iteritems():
              parse_value = category.split(".")[1]
              temp_data_storage_tma[parse_value] = data_value

            line_to_write = [
              temp_data_storage_tma["name"],
              temp_data_storage_tma["minthreshold"],
              temp_data_storage_tma["maxthreshold"],
              temp_data_storage_tma["icthreshold"]
            ]
            csv_writer.writerow(line_to_write)

      limits_save_file = Limits()
      limits_save_file.limits_type = type_of
      limits_save_file.filename = limitslist_name
      limits_save_file.file = os.path.join("limits", file_name_generator)
      limits_save_file.save()

  return HttpResponse("success")


@csrf_exempt
def ajax_uploaded_worklist(request, type_of):
  import csv

  if request.is_ajax():

    worklist_response_data = json.loads(request.body)

    media_path = os.path.join(settings.MEDIA_ROOT, "worklist")
    worklist_name = worklist_response_data['json']['worklist_name']
    submission_name = worklist_response_data['json']['submitter_name']

    file_name_generator = worklist_name + create_timestamp() + ".csv"
    file_save_path = os.path.join(media_path, file_name_generator)

    with open(file_save_path, "wb") as worklist_file:

      worklist_headers = ["term", "type", "logical vector"]

      if type_of == 'tma':
        worklist_headers = ["SearchTerm", "SampleType"]

      csv_writer = csv.writer(worklist_file, delimiter=",")

      csv_writer.writerow(worklist_headers)

      for key, value in worklist_response_data['json'].iteritems():
        if key == "worklist_name" or key == "submitter_name":
          continue
        else:

          # Temporary storage to parse the JSON data into a predictable format
          temp_data_storage = {
            "name": "",
            "type": "",
            "category": "",
          }

          if type_of == 'fusion':

            for category, data_value in value.iteritems():
              parse_value = category.split(".")[1]
              temp_data_storage[parse_value] = data_value

            line_to_write = [temp_data_storage["name"], temp_data_storage["type"],
                             temp_data_storage["category"]]

            csv_writer.writerow(line_to_write)


          else:

            for category, data_value in value.iteritems():

              parse_value = category.split(".")[1]
              temp_data_storage[parse_value] = data_value

            line_to_write = [temp_data_storage["name"], temp_data_storage["type"]]
            csv_writer.writerow(line_to_write)

      worklist_save_file = Worklist()
      worklist_save_file.worklist_type = type_of
      worklist_save_file.filename = worklist_name
      worklist_save_file.file = os.path.join("worklist", file_name_generator)
      worklist_save_file.save()

  return HttpResponse("success")

@csrf_exempt
def ajax_uploaded_recovery(request):
  import csv

  if request.is_ajax():

    recovery_response_data = json.loads(request.body)
    media_path = os.path.join(settings.MEDIA_ROOT, "recovery")
    recovery_name = recovery_response_data['json']['recovery_filename']
    submission_name = recovery_response_data['json']['submitter_name']

    file_name_generator = recovery_name + create_timestamp() + ".csv"
    file_save_path = os.path.join(media_path, file_name_generator)

    with open(file_save_path, "wb") as recovery_file:
      recovery_headers = ["Run.ID", "Lot.Number", "POL.truth", "LTR.truth"]

      csv_writer = csv.writer(recovery_file, delimiter=",")
      csv_writer.writerow(recovery_headers)

      for key, value in recovery_response_data['json'].iteritems():
        if key == 'recovery_filename' or key == 'submitter_name':
          continue
        else:
          temp_data_storage = {
            'runid':'',
            'lot':'',
            'pol':'',
            'ltr':''
          }

          for category, data_value in value.iteritems():
            parse_value = category.split(".")[1]
            temp_data_storage[parse_value] = data_value

          line_to_write = [
            temp_data_storage['runid'],
            temp_data_storage['lot'],
            temp_data_storage['pol'],
            temp_data_storage['ltr']
          ]

          csv_writer.writerow(line_to_write)

      recovery_save_file = RunRecovery()
      recovery_save_file.filename = recovery_name
      recovery_save_file.file = os.path.join("recovery", file_name_generator)
      recovery_save_file.save()
  return HttpResponse("success")


