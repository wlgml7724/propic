# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from tagging.fields import TagField
from propicker.models import *
from django.utils.text import slugify
from django.contrib.auth.models import User
from mysite.storage_backends import *
from hitcount.models import HitCountMixin
from django_random_queryset import RandomManager
from cart.models import *
from django.urls import reverse
from propicker.models import Propicker

from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile

class Photo(models.Model, HitCountMixin):
	user = models.ForeignKey(Propicker, on_delete=models.CASCADE)
	name = models.CharField('사진이름', max_length=200)
	ANIMAL = 0;
	PERSON = 1; 
	OBJECT = 2; 
	NATURE = 3;
	FOOD = 4;
	TRAVEL = 5;
	SEASON = 6;
	WEATHER = 7;
	CONSTRUCT = 8;
	MOVING = 9;
	ECT = 10;
	GENRE = (
	  (ANIMAL, '동물'),
	  (PERSON, '사람'),
	  (OBJECT, '사물'),
	  (NATURE, '풍경/자연'),
	  (FOOD, '음식'),
	  (TRAVEL, '여행'),
	  (SEASON, '계절'),
	  (WEATHER, '날씨'),
	  (CONSTRUCT, '건축'),
	  (MOVING, '동적 이미지'),
	  (ECT, '기타'),
	)   
	genre = models.IntegerField('장르', choices=GENRE)

	uploaded_at = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(upload_to='orgin', storage=MediaStorage())
	img_thumbnail = models.ImageField(upload_to='thumbnail/high', blank=True, storage=MediaStorage())
	img_thumbnail_d = models.ImageField(upload_to='thumbnail/down', blank=True, storage=MediaStorage())
	img_thumbnail_f = models.ImageField(upload_to='thumbnail/free', blank=True, storage=MediaStorage())
	content = models.TextField('사진 소개', max_length=260, null = True)
	tag = TagField()
	objects = RandomManager()
	price = models.IntegerField('사진 금액', default=0)
	create_date = models.DateTimeField('사진 작성일', auto_now_add=True)
	modify_date = models.DateTimeField('사진 수정일', auto_now = True, null=True)
	download_count = models.IntegerField('다운로드횟수', default=0)
	view_count=models.IntegerField('조회수', default=0)
	like_user_set = models.ManyToManyField(User,
                                   blank=True,
                                   related_name='like_user_set',
                                   through='Like') # post.like_set 으로 접근 가능
	cart_add = models.ManyToManyField('cart.Cart',
                                    blank = True,
                                    related_name='cart_add_set',
                                    through = 'cart.PhotoDetail')




	class META:
		verbose_name='사진'
		verbose_name_plural = '사진모음'
		ordering = ['-pk',  ]

	def make_thumbnail(self):
		size = (500, 500)

		f = MediaStorage().open(self.img.name)
		image = Image.open(f)
		ftype = image.format

		image = ImageOps.fit(image, size, Image.ANTIALIAS)

		path, ext = os.path.splitext(self.img.name)
		name = os.path.basename(path)

		thumbnail_name = '%s_thumb%s' % (name, ext)

		temp_file = BytesIO()
		image.save(temp_file, ftype)
		temp_file.seek(0)

		content_file = ContentFile(temp_file.read())
		self.img_thumbnail.save(thumbnail_name, content_file)

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

		thumbnail_name = '%s_thumb%s' % (name, ext)

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

		thumbnail_name = '%s_thumb%s' % (name, ext)

		temp_file = BytesIO()
		image.save(temp_file, ftype)
		temp_file.seek(0)

		content_file = ContentFile(temp_file.read())
		self.img_thumbnail_f.save(thumbnail_name, content_file)

		temp_file.close()
		content_file.close()
		f.close()

	def save(self, *args, **kwargs):
		image_changed = False

		if self.img and not self.img_thumbnail:
			image_changed = True

		if self.pk:
			# pk가 존재하면 pk에 해당하는 사진을 ori에 저장하라
			ori = Photo.objects.get(pk=self.pk)
			if ori.img != self.img:
				# 만약 ori.img와 현재 이미지가 다르면 이미지 변경을 실행하라
				image_changed = True

		super().save(*args, **kwargs)

		if image_changed:
			self.make_thumbnail()
			self.make_thumbnail2()
			self.make_thumbnail3()

	def __str__(self) :
		return '{}'.format(self.pk)

	def price_dpx(self):
		return (int)(self.price*0)

	def price_mpx(self):
		return (int)(self.price*0.5)

	def price_mhpx(self):
		return (int)(self.price*0.75)

	def get_absolute_url(self):
		return reverse('gallery:photo_detail', args=(self.id,))


	@property
	def like_count(self):
		return self.like_user_set.count()

        
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
    	return '{}'.format(self.user)

        


