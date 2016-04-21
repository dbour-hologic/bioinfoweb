from django.contrib import admin
from gparchives.models import Documents
# Register your models here.

class Documents_Admin(admin.ModelAdmin):

	model = Documents

	list_display = ('document_title', 'document_path',)

	def document_title(self, obj):
		return ("%s" % obj.title)
	document_title.short_description = "Document Title"

	def document_path(self, obj):
		return ("%s" % obj.document)
	document_path.short_description = "File Path"

admin.site.register(Documents, Documents_Admin)
