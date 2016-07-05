"""
Made for validation of file extensions for user-content
file uploads
"""

def validate_file_extension(value):

	import os
	from django.core.exceptions import ValidationError
	ext = os.path.splitext(value.name)[1]
	valid_extensions = ['.fasta','.txt','.text','.fas']
	if not ext.lower() in valid_extensions:
		raise ValidationError(u'Unsupported file extension. Please upload .fasta or .txt')