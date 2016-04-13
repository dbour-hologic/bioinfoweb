from django.shortcuts import render
from django.core.mail import send_mail
from .forms import msaeaccessForm

def index(request):
	return render(request, 'services/index_services.html')

def clone_services(request):
	return render(request, 'services/clone_services.html')

def msae_access(request):

	""" Used for submitting MSAE Access Requests
	This method is mainly for showing the form and posting data

	This method ties in with the following methods
	-- send_receipt() : used for sending an e-mail to supervisors for signature

	This method indirectly ties in with the following methods
	-- msae_access_approval_link() : used for generating approval link for specific users
	"""

	if request.method == 'POST':

		# Get hostname for send_receipt to build a link
		hostname = request.get_host()

		msae_access_form = msaeaccessForm(request.POST)
		if msae_access_form.is_valid():
			msae_access_form.save()
			return render(request, 'services/thanks.html')

	else:

		msae_access_form = msaeaccessForm()

	return render(request, 'services/msae_access.html', {'msaeaccessForm':msaeaccessForm})

def send_receipt(msae_form_data, hostname):

	""" Used to send an e-mail to the supervisor
	Takes in 
	-- msae_form_data - form data submitted after a POST request
	-- hostname - the host that initiated the POST request
	"""

	# List of e-mails 
	email_directory = {}
	email_directory['supervisor'] = (form_data.cleaned_data['supervisor_name'],
									 form_data.cleaned_data['supervisor_email'],)

	employee_name = form_data.cleaned_data['first_name'] + " " + form_data.cleaned_data['last_name']
	employee_network_name = form_data.cleaned_data['user_network_name']

	for user, userdata in email_directory.iteritems():

		approval_link = hostname + "/services/msaeaccess/" + employee_username
		email_msg = "Hello"

