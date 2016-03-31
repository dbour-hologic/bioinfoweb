from django.conf.urls import patterns, url
from services import views

urlpatterns = patterns('', url(r'^$', views.index, name='service_home'))