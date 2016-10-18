from django import forms
from .models import Worklist, Limits

class WorklistInputForm(forms.Form):

	class Meta:
		model = Worklist
		fields = ['file']

	file_upload_selection = forms.ModelChoiceField(
		queryset = Worklist.objects.all(),
		initial=1,
		widget=forms.Select(attrs={'class':'form-control'})

	)

class LimitsInputForm(forms.Form):

	class Meta:
		model = Limits
		fields = ['file']

	file_limits_upload_selection = forms.ModelChoiceField(
		queryset = Limits.objects.all(),
		initial=1,
		widget=forms.Select(attrs={'class':'form-control'})
	)