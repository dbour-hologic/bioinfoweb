from django.conf.urls import url
from seqconversion import views

urlpatterns = [
	url(r'^seqconversion/$', views.seq_tool, name='tools_seqconversion')
]
