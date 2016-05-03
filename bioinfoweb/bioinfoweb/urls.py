"""bioinfoweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from portal import urls as portal_urls
from services import urls as services_urls
from helpdesk import urls as helpdesk_urls
from tech import urls as tech_urls
from gparchives import urls as gparchives_urls
from seqconversion import urls as seqconversion_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^portal/', include(portal_urls)),
    url(r'^services/', include(services_urls)),
    url(r'^tech/', include(tech_urls)),
    url(r'^tech/', include(gparchives_urls)),
    url(r'^tools/', include(seqconversion_urls)),
]

# Third party applications
urlpatterns += [
    url(r'^helpdesk/', include(helpdesk_urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)