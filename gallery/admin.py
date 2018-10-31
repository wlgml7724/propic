from django.contrib import admin
from gallery.models import *
from django.contrib import admin
from image_cropping import ImageCroppingMixin

# Register your models here.

##admin.site.register(Photo)


##class PhotoAdmin(admin.ModelAdmin):
##    list_display = ('photo_name', 'owner')
##
##admin.site.register(Photo, PhotoAdmin)


class PhotoAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

admin.site.register(Photo, PhotoAdmin)
# admin.site.register(Photo)
admin.site.register(Like)
