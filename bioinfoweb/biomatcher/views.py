from django.shortcuts import render
from .forms import BiomatcherUploadForm, BiomatcherInputForm

def index(request):

	input_form = BiomatcherInputForm()

	return render(request, 'biomatcher/biomatcher.html', {"input_form":input_form})