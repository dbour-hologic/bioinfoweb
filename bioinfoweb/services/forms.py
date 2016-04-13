from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone

from .models import msaeaccess

class msaeaccessForm(forms.ModelForm):

	class Meta:

		model = msaeaccess
		fields = [
			'user_first_name', 'user_last_name', 'user_email',
			'user_network_name', 'user_title', 'user_location',
			'user_alt_location', 'user_status', 'user_contract_date',
			'phone_extension', 'request_type', 'date_required',
			'department_name', 'supervisor_name', 'supervisor_email',
			'employee_electronic_sig', 'employee_tos_agree'
		]

	common_req_attributes = {
		'class':'form-control input-sm required'
	}

	user_first_name = forms.CharField(
		label="First Name",
		widget=forms.TextInput(attrs=common_req_attributes)
	)

	user_last_name = forms.CharField(
		label="Last Name",
		widget=forms.TextInput(attrs=common_req_attributes)
	)

	user_email = forms.EmailField(
		label="User E-mail",
		widget=forms.TextInput(attrs={'class':'form-control input-sm required','type': 'email'})
	)

	user_network_name = forms.CharField(
		label="Username",
		widget=forms.TextInput(attrs=common_req_attributes),
		help_text="The username you use to log into your work computer"
	)

	user_title = forms.CharField(
		label="User Title",
		widget=forms.TextInput(attrs=common_req_attributes),
		help_text="ex: Research Associate, Scientist"
	)

	user_location = forms.ChoiceField(
		label="User Location",
		widget=forms.RadioSelect(attrs={'class':'required'}),
		choices=msaeaccess.user_location_choices
	)

	user_alt_location = forms.CharField(
		label="If other location selected, please specificy(if applicable)",
		widget=forms.TextInput(attrs={'class':'form-control input-sm'}),
		required=False
	)

	user_status = forms.ChoiceField(
		label="User Employment Status",
		widget=forms.RadioSelect(attrs={'class':'required'}),
		choices=msaeaccess.user_status_choices
	)

	user_contract_date = forms.DateTimeField(
		label="End of Employment Contract (if applicable)",
		widget=SelectDateWidget(),
		required=False,
	)

	phone_extension = forms.CharField(
		label="User Phone Extension",
		widget=forms.TextInput(attrs=common_req_attributes),
		required=False
	)

	request_type = forms.ChoiceField(
		label="Request Type",
		widget=forms.Select(attrs={'class':'required'}),
		choices=msaeaccess.request_type_choices
	)

	date_required = forms.DateTimeField(
		label="Date of Access Required",
		widget=SelectDateWidget(),
		initial=timezone.now(),
	)

	department_name = forms.CharField(
		label="Department Name",
		widget=forms.TextInput(attrs={'class':'form-control input-sm'}),
		required=False
	)

	supervisor_name = forms.CharField(
		label="Supervisor Name",
		widget=forms.TextInput(attrs=common_req_attributes)
	)

	supervisor_email = forms.EmailField(
		label="Supervisor E-mail",
		widget=forms.TextInput(attrs={'class':'form-control input-sm required', 'type':'email'})
	)

	employee_electronic_sig = forms.CharField(
		label="Employee Electronic Signature",
		widget=forms.TextInput(attrs=common_req_attributes),
	)

	employee_tos_agree = forms.BooleanField(
		label="Terms of Service",
		widget=forms.CheckboxInput(attrs={'class':'required'}),
		help_text="I agree to the terms of service."
	)	

class msae_supervisor_signature(forms.ModelForm):

	""" If user is coming from supervisor e-mail, provide this form for view """

	class Meta:

		model = msaeaccess
		fields = ['supervisor_electronic_sig', 'supervisor_date_signed']

	common_req_attributes = {
		'class':'form-control input-sm required'
	}

	supervisor_electronic_sig = forms.CharField(
		label="Supervisor E-Signature",
		widget=forms.TextInput(attrs=common_req_attributes)
	)

	supervisor_date_signed = forms.DateTimeField(
		label="Date",
		widget=SelectDateWidget(),
		initial=timezone.now()
	)


