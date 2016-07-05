from django.shortcuts import render
from .forms import BiomatcherUploadForm, BiomatcherInputForm

def index(request):

	if request.method == "POST":

		upload_form = BiomatcherUploadForm(request.POST, request.FILES)
		input_form = BiomatcherInputForm(request.POST)
		if upload_form.is_valid():
			upload_form.save()
	else:

		input_form = BiomatcherInputForm()
		upload_form = BiomatcherUploadForm()

	return render(request, 'biomatcher/biomatcher.html', {"input_form":input_form, "upload_form":upload_form})