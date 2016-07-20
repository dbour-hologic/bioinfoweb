from django.db import models
from .validators import validate_file_extension

class BiomatcherFileUpload(models.Model):

	biomatcher_filename = models.CharField(
		max_length=100,
		unique=True
	)

	biomatcher_fileupload = models.FileField(
		upload_to='biomatcher/database',
		validators=[validate_file_extension],
	)

	def __unicode__(self):
		return self.biomatcher_filename