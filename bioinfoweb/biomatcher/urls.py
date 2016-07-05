from django.conf.urls import url
from biomatcher import views

urlpatterns = [
	url(r'^$', views.index, name='biomatcher'),
	url(r'^run/$', views.matcher, name='biomatcher-run'),
]