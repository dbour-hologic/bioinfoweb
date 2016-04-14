from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'tech/tech_home.html')

def tech_tma(request):
	return render(request, 'tech/tech_tma.html')

def tech_invader(request):
	return render(request, 'tech/tech_invader.html')

