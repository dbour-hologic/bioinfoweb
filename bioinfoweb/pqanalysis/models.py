from django.db import models
from django.utils.timezone import now as timezone_now
import random
import string
import os

def upload_to(instance, filename):
	""" Custom upload modifier method that will help
	create a unique directory to store a group of files.
	The unique directory is generated by a name given
	by the user as well as a timestamp appended to the name.

	Args:
		instance - the file instance from post request (file obj)
		filename - the actual string representation of filename (str)
	Returns:
		the location to save the file (str)
	"""

	# base_media_dir = "files/media/pqanalysis/"
	save_directory = instance.analysis_id
	filename_base, filename_ext = os.path.splitext(filename)

	# new_implentation
	return "pqresults/" + save_directory + "/" + instance.analysis_id + "_" + filename_base + filename_ext.lower()
	# old_implementation - before name change
	# return "pqresults/" + save_directory + "/" + filename_base + filename_ext.lower()

class PqAttachment(models.Model):
	analysis_id = models.CharField(max_length=100)
	file_name = models.CharField(max_length=100)
	attachment = models.FileField(upload_to=upload_to, max_length=1000)
	submitter = models.CharField(max_length=100)
	date_submitted = models.DateField(auto_now_add=True)
	
class PqResults(models.Model):
	pqresults = models.ForeignKey(PqAttachment, on_delete=models.CASCADE)
	pq_file_name = models.CharField(max_length=100)
	file_dir = models.FileField(upload_to=None, max_length=1000)

class CombineResults(models.Model):
	combine_file_name = models.CharField(max_length=100)
	combine_file_dir = models.FileField(upload_to="pqcombined", max_length=1000)
	date_uploaded = models.DateField(auto_now_add=True)

class Worklist(models.Model):
	""" Storing user worklist """
	filename = models.CharField(max_length=1000)
	file = models.FileField(upload_to="worklist")
	slug = models.SlugField(max_length=1000, blank=True)
	upload_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.filename

	def __unicode__(self):
		return self.filename

	def get_absolute_url(self):
		return ('upload-delete',)

	def save(self, *args, **kwargs):
		self.slug = self.file.name
		super(Worklist, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.file.delete(False)
		super(Worklist, self).delete(*args, **kwargs)

class Limits(models.Model):
	""" Storing user worklist """
	filename = models.CharField(max_length=1000)
	file = models.FileField(upload_to="limits")
	slug = models.SlugField(max_length=1000, blank=True)
	upload_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.filename

	def __unicode__(self):
		return self.filename

	def get_absolute_url(self):
		return ('upload-delete',)

	def save(self, *args, **kwargs):
		self.slug = self.file.name
		super(Limits, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.file.delete(False)
		super(Limits, self).delete(*args, **kwargs)
