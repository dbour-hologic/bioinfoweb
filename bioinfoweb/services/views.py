from django.shortcuts import render
from .forms import msaeaccessForm

def index(request):
	return render(request, 'services/index_services.html')

def clone_services(request):
	return render(request, 'services/clone_services.html')

def msae_access(request):

	if request.method == 'POST':

		hostname = request.get_host()

	else:

		msae_access_form = msaeaccessForm()

	return render(request, 'services/msae_access.html', {'msaeaccessForm':msaeaccessForm})