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
  url(r'^prepopulate-worklist-tma/(?P<pk>\d+)$', views.worklist_get_tma, name='pptma-worklist'),
  url(r'^prepopulate-limitslist-tma/(?P<pk>\d+)$', views.limitslist_get_tma, name='pptma-limitslist'),
  url(r'^prepopulate-recovery-tma/(?P<pk>\d+)$', views.recovery_get_tma, name='pptma-recovery'),
  url(r'^worklist-upload/(?P<type_of>\w+)/$', views.ajax_uploaded_worklist, name='ajax-upload-worklist'),
  url(r'^limits-upload/(?P<type_of>\w+)/$', views.ajax_uploaded_limits, name='ajax-upload-limits'),
  url(r'^recovery-upload/$', views.ajax_uploaded_recovery, name='ajax-upload-recovery'),
  url(r'^limitslist/$', views.get_limitslist_update, name='update-limitslist'),
  url(r'^recoverylist/$', views.get_recovery_update, name='update-recoverylist')
]
