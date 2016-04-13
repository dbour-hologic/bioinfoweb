from django.shortcuts import render
from .forms import msaeaccessForm

def index(request):
	return render(request, 'services/index_services.html')

def clone_services(request):
	return render(request, 'services/clone_services.html')

def msae_access(request):

	if request.method == 'POST':

		msae_access_form = msaeaccessForm(request.POST)
		if msae_access_form.is_valid():
			msae_access_form.save()
			return render(request, 'services/thanks.html')
		print "Did not pass validation"

	else:

		msae_access_form = msaeaccessForm()

	return render(request, 'services/msae_access.html', {'msaeaccessForm':msaeaccessForm})