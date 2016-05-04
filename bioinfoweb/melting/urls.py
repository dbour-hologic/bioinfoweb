from django.conf.urls import patterns, url
from . import views

urlpatterns = [
	 url(r'^melting/$', views.ajaxtest, name='tools_melting'),
	 url(r'^meltingresponse/$', views.ajaxresponse, name='tools_melting_response'),
]
