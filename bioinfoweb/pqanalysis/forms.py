from django import forms
from .models import Worklist

class WorklistInputForm(forms.Form):

	class Meta:
		model = Worklist
		fields = ['file']

	file_upload_selection = forms.ModelChoiceField(
		queryset = Worklist.objects.all(),
		initial=1,
		widget=forms.Select(attrs={'class':'form-control'})

	)