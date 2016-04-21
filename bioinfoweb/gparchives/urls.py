from django.conf.urls import url
from gparchives import views

urlpatterns = [ url(r'^gparchives/$', views.index, name='tech_archives'),
]