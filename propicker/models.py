# -*- coding: utf-8 -*-
# 표준 라이브러리 임포트
# 여러 모듈이 같은 이름을 가질 때 당신이 모듈을 임포팅 하는것을 보장해줍니다.
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
# 코어 장고 임포트
from django.db import models
from django.contrib.auth.models import User
from mysite.storage_backends import *
from django.urls import reverse


from django.db.models.signals import post_save
from django.dispatch import receiver

class PropickerManager(models.Manager):
    
    def get_propicker_photo(self):
        return self.get_object(photo)


class Propicker(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    auto_login=models.BooleanField('로그인유지여부', default=False)
    # name=models.CharField('회원이름', max_length=30, null=False)
    phone=models.CharField('회원 전화번호', max_length=30, null=True)
    birth=models.DateField('생년월일', null=True, blank = True)
    MALE=True;
    FEMALE=False;
    USER_SEX_CHOICE=(
            (MALE, '남자'),
            (FEMALE, '여자')
    )
    isMale=models.BooleanField('성별(Default: 남자)', choices=USER_SEX_CHOICE, default=True)
    content=models.TextField('회원소개', max_length=200, null=True, blank=True)
    upload = models.FileField(storage=Public1MediaStorage(), blank = True)
    NORMAL ='no'; 
    PAUSE ='pa'; 
    STOP ='st';
    QUIT = 'qu';
    STATE_CHOICE=(
            (NORMAL, '일반'),
            (PAUSE, '일시정지'), 
            (STOP, '영구정지'),
            (QUIT, '탈퇴')
    )
    user_state=models.CharField("회원상태", max_length=2, choices=STATE_CHOICE, default="no")
    kakao_use=models.BooleanField('카카오사용여부', default=False)
    naver_use=models.BooleanField('네이버사용여부', default=False)
    like_user_set = models.ManyToManyField('self',
                                   blank=True,
                                   related_name='Propicker.like_user_set+',
                                   through='UserLike', symmetrical=False) # post.like_set 으로 접근 가능
    # propicker_like=models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    
    objects=PropickerManager()

    class Meta:
            verbose_name = 'propicker'
            verbose_name_plural = 'propickers'
            ordering = ['pk', ]

    def __str__(self) :
            return '{}'.format(self.pk)

    def get_user_image(self):
            return self.user_image
    @property
    def like_count(self):
        return self.to_propicker.count()


    # def get_user_from_phone(self, input_phone):
    #     print("입력값", input_phone)
    #     # print(self.objects.get(self.phone = input_phone))
    #     if self.objects.get(self.phone = input_phone):
    #         print("if 실행")
    #         print(self.phone)
    #         return self.user
    #     return "해당되는 값이 없습니다."



                
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Propicker.objects.create(user=instance)
        instance.propicker.save()
##

class UserAccount(models.Model):
    user = models.ForeignKey(Propicker, on_delete=models.CASCADE)
    # 계좌번호
    user_account_num = models.IntegerField('계좌번호')
    # 은행이름
    user_account_bank = models.CharField('은행이름', max_length=10)
    

        
class UserLike(models.Model):
    like_user = models.ForeignKey(Propicker, on_delete=models.CASCADE, related_name='from_propicker')
    receive_user = models.ForeignKey(Propicker, on_delete=models.CASCADE, related_name='to_propicker')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return '{}'.format(self.like_user)

