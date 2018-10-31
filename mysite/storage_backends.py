from storages.backends.s3boto3 import S3Boto3Storage
from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image, ImageOps
import os


class MediaStorage(S3Boto3Storage):
    location = 'media/gallery'
    file_overwrite = False

class PublicMediaStorage(S3Boto3Storage):
    location = 'media/theme'
    file_overwrite = False

class Public1MediaStorage(S3Boto3Storage):
    location = 'media/propicker'
    file_overwrite = False