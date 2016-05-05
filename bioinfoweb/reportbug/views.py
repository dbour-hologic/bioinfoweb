from django.shortcuts import render
from .forms import ReportBugForm

def bug(request):

	if request.method == "POST":
		reportBug = ReportBugForm(request.POST)
		if reportBug.is_valid():
			reportBug.save()
			return render(request, 'reportbug/thanks.html')
	else:
		reportBug = ReportBugForm()

	return render(request, 'reportbug/reportbug.html', {'reportBug':reportBug})
