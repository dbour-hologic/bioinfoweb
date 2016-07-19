from django import forms
from .models import BiomatcherFileUpload

class BiomatcherUploadForm(forms.ModelForm):
	
	class Meta:
		model = BiomatcherFileUpload
		fields = ['biomatcher_fileupload', 'biomatcher_filename']

class BiomatcherInputForm(forms.Form):

	# Enter sequences in FASTA format
	patterns = forms.CharField(
		widget = forms.Textarea
	)

	# Number of mismatches set for the search
	max_mismatches_allowed = forms.IntegerField(
		initial = 0
	)

	# A cutoff for the amount of times a pattern matches with a single subject
	minimum_total_hits = forms.IntegerField(
		initial = 0
	)

	# A cutoff for the amount of times a pattern matches with a single subject
	maximum_total_hits = forms.IntegerField(
		initial = 0
	)

	# Displays the uploaded files
	file_upload_selection = forms.ModelMultipleChoiceField (
		queryset = BiomatcherFileUpload.objects.order_by('-id')
	)

