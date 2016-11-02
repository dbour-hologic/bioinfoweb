from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.add_attachment, name='add_attachment'),
	url(r'^results/$', views.view_results, name='view_results'),
	url(r'^upload/$', views.worklist_upload, name='upload-new'),
	url(r'^delete-worklist/(?P<pk>\d+)$', views.worklist_delete, name='upload-delete'),
	url(r'^worklist/$', views.get_worklist_update, name='update-worklist'),
	url(r'^prepopulate-worklist/(?P<pk>\d+)$', views.worklist_get, name='pp-worklist'),
	url(r'^prepopulate-limitslist/(?P<pk>\d+)$', views.limitslist_get, name='pp-limitslist'),
	url(r'^worklist-upload/$', views.ajax_uploaded_worklist, name='ajax-upload-worklist'),
	url(r'^limits-upload/$', views.ajax_uploaded_limits, name='ajax-upload-limits'),
	url(r'^limitslist/$', views.get_limitslist_update, name='update-limitslist')
]