from django import forms
from .models import ReportBug

class ReportBugForm(forms.ModelForm):

	class Meta:
		model = ReportBug
		fields = ['bug_reporter_name', 'bug_title', 'bug_description']

	bug_reporter_name = forms.CharField(
		required=False,
		label="Name",
		widget=forms.TextInput(attrs={'class':'form-control input-sm'}), help_text="Name(Optional)"
	)

	bug_title = forms.CharField(
		label="Title", 
		widget=forms.TextInput(attrs={'class':'form-control input-sm required'})
	)
	
	bug_description=forms.CharField(
		label="Description",
		widget=forms.Textarea(attrs={'class':'form-control input-sm required'})
	)

