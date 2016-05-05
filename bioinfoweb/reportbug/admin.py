from django.contrib import admin

from reportbug.models import ReportBug

class report_bug_admin(admin.ModelAdmin):

	model = ReportBug
	list_display = ('bug_title',)

	def bug_title(self, obj):
		return ("%s" % (obj.bug_title))
	bug_title.short_description = "Bug Title"

admin.site.register(ReportBug, report_bug_admin)
