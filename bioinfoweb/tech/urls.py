from django.conf.urls import patterns, url
from tech import views

urlpatterns = [	url(r'^$', views.index, name='tech_home'),
		url(r'^tma/$', views.tech_tma, name='tech_tma'),
		url(r'^invader/$', views.tech_invader, name='tech_invader'),
]
