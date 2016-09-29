from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.add_attachment, name='add_attachment'),
	url(r'^results/$', views.view_results, name='view_results'),
	url(r'^upload/$', views.worklist_upload, name='upload-new'),
	url(r'^delete-worklist/(?P<pk>\d+)$', views.worklist_delete, name='upload-delete'),
	url(r'^worklist/$', views.get_worklist_update, name='update-worklist'),
	url(r'^worklist-upload/$', views.ajax_uploaded_worklist, name='ajax-upload-worklist')
]