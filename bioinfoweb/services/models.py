from django.db import models

# Create your models here.
class msaeaccess(models.Model):
	""" Used for requesting permission to use MSAE. """

	request_type_choices = (
		("New Account", "New Account"),
		("Remove Existing Account","Remove Existing Account"),
	)

	user_status_choices = (
		("Full Time", "Full Time"),
		("Temporary", "Temporary"),
		("Consultant", "Consultant"),
	)

	user_location_choices = (
		("GCD1","GCD1"),
		("GCD2","GCD2"),
		("Other","Other"),
	)

	user_first_name = models.CharField(
		max_length=100
	)

	user_last_name = models.CharField(
		max_length=100
	)

	user_email = models.CharField(
		max_length=100
	)

	user_network_name = models.CharField(
		max_length=100,
		unique=True
	)

	user_title = models.CharField(
		max_length=100
	)

	user_location = models.CharField(
		max_length=100,
		choices=user_location_choices,
		null=True,
		blank=True
	)

	user_alt_location = models.CharField(
		max_length=100,
		null=True,
		blank=True
	)

	request_type = models.CharField(
		max_length=100,
		choices=request_type_choices
	)

	request_date = models.DateField(
		auto_now_add=True
	)

	date_required = models.DateField()

	user_status = models.CharField(
		max_length=100,
		choices=user_status_choices
	)

	user_contract_date = models.DateField(
		null=True,
		blank=True
	)

	phone_extension = models.CharField(
		max_length=100
	)

	department_name = models.CharField(
		max_length=100
	)

	supervisor_name = models.CharField(
		max_length=100
	)

	supervisor_email = models.CharField(
		max_length=100
	)

	employee_electronic_sig = models.CharField(
		max_length=100,
		default=""
	)

	employee_tos_agree = models.BooleanField()

	employee_date_signed = models.DateField(
		auto_now_add=True
	)

	# Confirmation Usage Only -- Not Viewed in Request Form

	supervisor_electronic_sig = models.CharField(
		max_length=100,
		default=""
	)

	supervisor_signed = models.BooleanField()

	# Bioinformatics Admin Use Only

	date_approved = models.DateField(
		blank=True,
		null=True
	)

	approver_name = models.CharField(
		max_length=100,
		blank=True
	)

	class Meta:
		verbose_name = "MSAE Request"