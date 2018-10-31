from django.conf.urls import url
from . import views
from mypic.views import *
app_name='mypic'
urlpatterns = [

    # Example: /
    url(r'^$', MypicLV.as_view(), name='index'),

]