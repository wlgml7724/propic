# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from gallery.models import Photo
from django.conf import settings
from django.contrib.auth.models import User

from mysite.storage_backends import *


# Create your models here.
# 테마 ______________________________________________________________________________________________________________________________________________
# 테마 Theme
class Theme(models.Model):
	# 테마명
	theme_title = models.CharField('테마명', max_length=30) # 테마명
	# 테마대표사진
	theme_img = models.FileField(storage=PublicMediaStorage())
	# 테마 설명
	theme_content = models.TextField('테마설명') # 테마설명
	# 사진번호
	photo_id = models.ManyToManyField(Photo) #  사진번호(FK)
	# 테마 게시일
	theme_create_date = models.DateTimeField('테마 작성일', auto_now_add=True)
	# 테마 수정일
	theme_modify_date = models.DateTimeField('테마 수정일', auto_now = True, null=True)

	class Meta:
		verbose_name = '테마'
		verbose_name_plural = '테마모음'
		ordering = ['pk', ]
	def __str__(self):
		return '{}'.format( self.photo_id)
	def get_absolute_url(self):
		return reverse('theme:theme_detail', args=(self.id,))




