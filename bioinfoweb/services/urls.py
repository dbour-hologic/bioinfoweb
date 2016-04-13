from django.conf.urls import patterns, url
from services import views

urlpatterns = [ url(r'^$', views.index, name='service_home'),
				url(r'^clone$', views.clone_services, name='clone_services'),
				url(r'^msaeaccess$', views.msae_access, name='msae_access'),
]