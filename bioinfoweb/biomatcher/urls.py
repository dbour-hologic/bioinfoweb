from django.conf.urls import url
from biomatcher import views

urlpatterns = [
	url(r'^$', views.index, name='biomatcher'),
]