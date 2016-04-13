from django.shortcuts import render

def index(request):
	return render(request, 'services/index_services.html')

def clone_services(request):
	return render(request, 'services/clone_services.html')