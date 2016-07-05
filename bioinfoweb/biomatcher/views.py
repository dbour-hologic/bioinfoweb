from django.shortcuts import render
from .forms import BiomatcherUploadForm, BiomatcherInputForm

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

	# Add implementation for matcher
	# Make a hidden form to take value from dropdown select
	# Use javascript to submit it all in one form
	# Example: stackoverflow.com/questions/1759006/embed-an-html-form-within-a-larger-form
	print request.POST

	return render(request, 'biomatcher/biomatcher_run.html')