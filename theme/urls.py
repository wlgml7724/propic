"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url

from theme.views import *

app_name = 'theme'
urlpatterns = [

    # Example: /
    url(r'^$', ThemeLV.as_view(), name='index'),

    # Example: /theme/, same as /
    url(r'^theme/$', ThemeLV.as_view(), name='theme_list'),

    # Example: /theme/99/
    url(r'^theme/(?P<pk>\d+)/$', ThemeDV.as_view(), name='theme_detail'),

    # Example : /99/update/
    url(r'^(?P<pk>[0-9]+)/update/$', ThemePhotoUpdateView.as_view(), name='theme_update'),

    # # Example : 99/delete/
    # url(r'^(?P<pk>[0-9]+)/delete/$', ThemePhotoDeleteView.as_view(), name='delete',),
]
