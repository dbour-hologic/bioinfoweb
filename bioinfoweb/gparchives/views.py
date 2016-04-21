from django.shortcuts import render
from .models import Documents

# Create your views here.
def index(request):

	archive_list = Documents.objects.all()

	return render(request, 'gparchives/tech_archives.html', {"archive_list":archive_list},)