from django.db import models

class ReportBug(models.Model):
	""" All bug reports are registered
	here.
	"""

	class Meta:
		verbose_name = "Bug Report"

	bug_reporter_name = models.CharField(
		max_length=100
	)

	bug_title = models.CharField(
		max_length=100
	)

	bug_description = models.TextField(
		null=True
	) 