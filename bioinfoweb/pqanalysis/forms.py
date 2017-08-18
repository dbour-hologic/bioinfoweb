from django import forms
from .models import Worklist, Limits, RunRecovery


class RunRecoveryForm(forms.Form):
  class Meta:
    model = RunRecovery
    fields = ['file']

  file_upload_selection_recovery = forms.ModelChoiceField(
    queryset=RunRecovery.objects.all(),
    initial=1,
    widget=forms.Select(attrs={'class':'form-control'})
  )


class WorklistInputForm(forms.Form):
  class Meta:
    model = Worklist
    fields = ['file']

  file_upload_selection = forms.ModelChoiceField(
    queryset=Worklist.objects.filter(worklist_type__iexact='fusion'),
    initial=1,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  file_upload_selection_tma = forms.ModelChoiceField(
    queryset=Worklist.objects.filter(worklist_type__iexact='tma'),
    initial=1,
    widget=forms.Select(attrs={'class': 'form-control'})
  )


class LimitsInputForm(forms.Form):
  class Meta:
    model = Limits
    fields = ['file']

  file_limits_upload_selection = forms.ModelChoiceField(
    queryset=Limits.objects.filter(limits_type__iexact='fusion'),
    initial=1,
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  file_limits_upload_selection_tma = forms.ModelChoiceField(
    queryset=Limits.objects.filter(limits_type__iexact='tma'),
    initial=1,
    widget=forms.Select(attrs={'class': 'form-control'})
  )
