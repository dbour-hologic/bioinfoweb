from django.db import models

class BiomatcherFileUpload(models.Model):

	biomatcher_filename = models.CharField(
		max_length=100,
		unique=True
	)

	biomatcher_fileupload = models.FileField(
		upload_to='biomatcher/database'
	)

	def __unicode__(self):
		return self.biomatcher_filename