from django import forms
from .models import BiomatcherFileUpload



class BiomatcherUploadForm(forms.ModelForm):
	
	class Meta:
		model = BiomatcherFileUpload
		fields = ['biomatcher_fileupload', 'biomatcher_filename']

	biomatcher_fileupload = forms.FileField(
		widget=forms.FileInput(
			attrs={'class':'required'}
		)
	);
	biomatcher_filename = forms.CharField(
		widget=forms.TextInput(
			attrs={'class':'required'}
		)
	)

class BiomatcherInputForm(forms.Form):

	class Meta:
		model = BiomatcherFileUpload
		fields = ['file_upload_selection']

	# Enter sequences in FASTA format
	patterns = forms.CharField(
		widget = forms.Textarea()
	)

	# Number of mismatches set for the search
	max_mismatches_allowed = forms.IntegerField(
		initial = 0
	)

	# A cutoff for the amount of times a pattern matches with a single subject
	minimum_total_hits = forms.IntegerField(
		initial = 1
	)

	# A cutoff for the amount of times a pattern matches with a single subject
	maximum_total_hits = forms.IntegerField(
		initial = 1
	)

	# Displays the uploaded files
	file_upload_selection = forms.ModelChoiceField (
		queryset = BiomatcherFileUpload.objects.order_by('-id')
	)

	# Modify init to remove blank selection field and replace with a message.
	def __init__(self, *args, **kwargs):
		super(BiomatcherInputForm, self).__init__(*args,**kwargs)
		modelchoicefields = [field for fieldname, field in self.fields.iteritems() if isinstance(field, forms.ModelChoiceField)]

		for field in modelchoicefields:
			field.empty_label = "Please select a database"