from django.conf.urls import url
from . import views
from gallery.views import *
app_name='gallery'
urlpatterns = [

    # Example: /
    url(r'^$', GalleryLV.as_view(), name='index'),

   # Example: /photo/99/
    url(r'^gallery/(?P<pk>\d+)/$', GalleryDV.as_view(), name='photo_detail'),
    url(r'^gallery/payment/$', views.add_photo_payment, name='add_photo_payment'), 
    url(r'^cartadd/$', views.cart_add, name='cart_add'), 
    

    # Example: /tag/
    url(r'^tag/$', TagTV.as_view(), name='tag_cloud'),  

    # Example: /tag/tagname/
    url(r'^tag/(?P<tag>[^/]+(?u))/$', GalleryTOL.as_view(), name='tagged_object_list'),

    # Example: /search/
    url (r'^search/$', SearchFormView.as_view(), name='search'),

    # Example : /add/
    url(r'^add/$', GalleryCreateView.as_view(), name='add',),

     # Example : /change/
    url(r'^change/$', GalleryChangeLV.as_view(), name='change',),

    # Example : /99/update/
    url(r'^(?P<pk>[0-9]+)/update/$', GalleryUpdateView.as_view(), name='update',),

    # Example : 99/delete/
    url(r'^(?P<pk>[0-9]+)/delete/$', GalleryDeleteView.as_view(), name='delete',),

    url(r'^like/$', views.photo_like, name='photo_like'), 

    url(r'^mlike/$', GalleryLikeLV.as_view(), name='photo_likes'), 

    url(r'^download/$', views.downloader, name='download'),     

    
]