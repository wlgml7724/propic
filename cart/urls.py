from django.conf.urls import url, include
from .views import *
from . import views
from django.urls import path

app_name = 'cart'

# 카트로 가는 url
urlpatterns = [
     path('detail/', views.detail, name="detail"),
     path('payment/', PG.as_view(), name="payment" ),
     path('delete/<pk>', photoDelete.as_view(), name='delete'),
     path('download/', views.get_download_photos, name='get-down-photo')
     # path('classDetail/', CartDetail.as_view()),
     # path('detail/', PersonalCart.as_view()),
]
