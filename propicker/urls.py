from django.conf.urls import url
from .views import *
from . import views

from django.urls import path
from calculate.views import *

app_name = 'propicker'
urlpatterns = [
     # Example : Propicker/

     url(r'^$', PropickerLV.as_view(), name='index'),

     # Example : Propicker/rank
     url(r'^rank/$', RankLV.as_view(), name='rank'),

     # Example : Propicker/5/
     url(r'^propicker/(?P<pk>\d+)/$', views.propicker_detail, name='detail'),
     url(r'^account/$', views.account_create, name='account'),
     url(r'^account/(?P<pk>\d+)/update/$', views.account_update, name='account_update'),
     url(r'^account/(?P<pk>\d+)/delete/$', views.account_delete, name='account_delete'),

     url(r'^id/$', IDSearchFormView.as_view(), name='idsearch'),
     url(r'^pw/$', PWSearchFormView.as_view(), name='pwsearch'),
     url(r'^like/$', views.user_like, name='user_like'), 

     url(r'^setting/$', SettingView.as_view(), name='setting'), 
     url(r'^user/(?P<pk>\d+)/update/$', views.user_update, name='user_update'), 
     url(r'^profile/(?P<pk>\d+)/update/$', views.profile_update, name='profile_update'),
]
