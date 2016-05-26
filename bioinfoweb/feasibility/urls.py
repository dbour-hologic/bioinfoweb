from django.conf.urls import url
from feasibility import views

urlpatterns = [ url(r'^feasibility_archives/$', views.index, name='feasibility_archives'),
]
