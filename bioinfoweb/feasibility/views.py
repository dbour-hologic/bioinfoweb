from django.shortcuts import render
from .models import FeasibilityDocuments

# Create your views here.
def index(request):

	archive_list = FeasibilityDocuments.objects.all()

	return render(request, 'feasibility/feasibility.html', {"archive_list":archive_list},)
