from django.db import models
import datetime

# Creates a range of years to use for year selection
YEAR_CHOICES = [(yr,yr) for yr in range(1960, datetime.datetime.now().year+1)] 

# Create your models here.
class FeasibilityDocuments(models.Model):
	document = models.FileField(
		max_length=2000,
		upload_to='feasibility',
	)

	title = models.CharField(
		max_length=2000,
		null=True,
		blank=True,
	)

	author = models.CharField(
		max_length=2000,
		null=True,
		blank=True,
	)

	year = models.IntegerField(
		choices=YEAR_CHOICES,
		null=True,
		blank=True,
	)

	keywords = models.CharField(
		max_length=2000,
		null=True,
		blank=True,
	)

	def __unicode__(self):
		return self.title
