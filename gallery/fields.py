from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image, ImageOps
import os

from mysite.storage_backends import *

from django.core.files.storage import default_storage as storage
from django.core.files.storage import default_storage


class ThumbnailImageFieldFile(ImageFieldFile):
    def make_thumbnail(self):
        size = (500, 500)
        f = MediaStorage().open(self.name)
        image = Image.open(f)
        ftype = image.format
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        path, ext = os.path.splitext(self.img.name)
        name = os.path.basename(path)
        thumbnail_name = '%s_thumb_high%s' % (name, ext)
        temp_file = BytesIO()
        image.save(temp_file, ftype)
        temp_file.seek(0)
        content_file = ContentFile(temp_file.read())
        self.img_thumbnail_h.save(thumbnail_name, content_file)
        temp_file.close()
        content_file.close()
        f.close()
    def make_thumbnail2(self):
        size = (400, 400)
        f = MediaStorage().open(self.img.name)
        image = Image.open(f)
        ftype = image.format
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        path, ext = os.path.splitext(self.img.name)
        name = os.path.basename(path)
        thumbnail_name = '%s_thumb_down%s' % (name, ext)
        temp_file = BytesIO()
        image.save(temp_file, ftype)
        temp_file.seek(0)
        content_file = ContentFile(temp_file.read())
        self.img_thumbnail_d.save(thumbnail_name, content_file)
        temp_file.close()
        content_file.close()
        f.close()
    def make_thumbnail3(self):
        size = (300, 300)
        f = MediaStorage().open(self.img.name)
        image = Image.open(f)
        ftype = image.format
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        path, ext = os.path.splitext(self.img.name)
        name = os.path.basename(path)
        thumbnail_name = '%s_thumb_free%s' % (name, ext)
        temp_file = BytesIO()
        image.save(temp_file, ftype)
        temp_file.seek(0)
        content_file = ContentFile(temp_file.read())
        self.img_thumbnail_f.save(thumbnail_name, content_file)
        temp_file.close()
        content_file.close()
        f.close()

    def save(self, *args, **kwargs):
        
            self.make_thumbnail()
            self.make_thumbnail2()
            self.make_thumbnail3()
    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super(ThumbnailImageFieldFile, self).delete(save)


class ThumbnailImageField(ImageField):
    attr_class = ThumbnailImageFieldFile
    

    def __init__(self, thumb_width=128, thumb_height=128, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super(ThumbnailImageField, self).__init__(*args, **kwargs)
