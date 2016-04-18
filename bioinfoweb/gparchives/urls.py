from django.conf.urls import url
from gparchives import views

urlpatterns = [ url(r'^$', views.index, name='tech_archives'),
]