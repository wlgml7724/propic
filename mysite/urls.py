"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from gallery.views import *
from django.contrib import admin
from django.conf.urls import include, url

from django.conf.urls.static import static
from django.conf import settings

from mysite import views as core_views
from mysite.views import HomeView
from mysite.views import *
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')), 
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', core_views.signup, name='signup'),
    # url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/allauth/', include('allauth.urls')),
    url(r'^accounts/register/$', UserCreateView.as_view(), name='register'),
    url(r'^accounts/register/done/$', UserCreateDoneTV.as_view(), name='register_done'),
    url(r'^accounts/register/before/$', UserCreateBefore.as_view(), name='register_before'),

    
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^propicker/', include('propicker.urls', namespace='propicker')),
    url(r'^gallery/', include('gallery.urls', namespace='gallery')),
    url(r'^theme/', include('theme.urls', namespace='theme')),
    url(r'^mypic/', include('mypic.urls', namespace='mypic')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^qna/', include('qna.urls', namespace='qna')),
    url(r'^calculate/', include('calculate.urls', namespace='calculate')),
]
