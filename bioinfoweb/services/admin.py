from django.contrib import admin

from services.models import msaeaccess

class msae_admin(admin.ModelAdmin):

	model = msaeaccess

	list_display = (
		'upper_case_name', 'username', 'userinfo',
		'dateformat', 'super_signature', 'approver_name',
		'approver_date'
	)

	list_filter = ['request_date']

	def upper_case_name(self, obj):
		return ("%s, %s" % (obj.user_last_name, obj.user_first_name)).upper()
	upper_case_name.short_description = "Name"

	def dateformat(self, obj):
		return ("%s" % obj.request_date)
	dateformat.short_description = "Request Date"

	def userinfo(self, obj):
		return ("E-mail: %s | Phone Ext: %s" % (obj.user_email, obj.phone_extension))
	userinfo.short_description = "User Information"

	def username(self, obj):
		return ("%s" % (obj.user_network_name)).upper()
	username.short_description = "User Name"

	def super_signature(self, obj):
		return ("%s" % (obj.supervisor_signed))
	super_signature.short_description = "Supervisor Approved"

	def approver_name(self, obj):
		return ("%s" % (obj.approver_name))
	approver_name.short_description = "Approver Name"

	def approver_date(self, obj):
		return ("%s" % (obj.date_approved))
	approver_date.short_description = "Approval Date"

admin.site.register(msaeaccess, msae_admin)