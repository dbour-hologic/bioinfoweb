from django import forms
from .models import Worklist, Limits, RecoveryRate


class WorklistInputForm(forms.Form):
  class Meta:
    model = Worklist
    fields = ['file']

  # Separate out the worklist to display from the different assay types
  file_upload_selection_tma = forms.ModelChoiceField(
    queryset=Worklist.objects.filter(worklist_type__iexact='tma'),
    initial=1,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  file_upload_selection_fusion = forms.ModelChoiceField(
    queryset=Worklist.objects.filter(worklist_type__iexact='fusion'),
    initial=1,
    widget=forms.Select(attrs={'class': 'form-control'})
  )


class RecoveryRateInputForm(forms.Form):
  class Meta:
    model = RecoveryRate
    fields = ['file']

  recovery_file_upload = forms.ModelChoiceField(
    queryset=RecoveryRate.objects.all(),
    initial=1,
    widget=forms.Select(attrs={'class': 'form-control'})
  )


class LimitsInputForm(forms.Form):
  class Meta:
    model = Limits
    fields = ['file']

  file_limits_upload_selection_tma = forms.ModelChoiceField(
    queryset=Limits.objects.filter(limits_type__iexact='tma'),
    initial=1,
    widget=forms.Select(attrs={'class': 'form-control'})
  )


  file_limits_upload_selection_fusion = forms.ModelChoiceField(
    queryset=Limits.objects.filter(limits_type__iexact='fusion'),
    initial=1,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
