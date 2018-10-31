from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType


from gallery.models import *
from propicker.models import Propicker
from django.contrib.auth.models import User


class Payment(models.Model):
    date=models.DateTimeField("결제일자", auto_now_add=True)
    method = models.CharField('결제방식', max_length=20, null=True)
    price = models.PositiveIntegerField('결제금액', default=0)
    merchant_uid = models.CharField('고유주문번호', max_length=30, null=True, blank=True, default=None)
    photo = models.OneToOneField('gallery.Photo', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='buy_one', unique=False)
    
    class Meta:
        verbose_name = ('payment')
        verbose_name_plural = ('payments')
        ordering = ('-date',)   

    def __str__(self):
        return '{}'.format(self.pk)

    def save_payment(self, payment_method, price, uid):
        self.method = payment_method
        self.price = price
        self.merchant_uid = uid
        return super().save(self)


class CartManager(models.Manager):
    def get_cart(self):
        # payment가 null인 cart를 가져와라
        return self.exclude(payment__isnull=False)
        
    def get_cart_show(self):
        # payment가 null이 아닌 cart를 가져와라 
        return self.exclude(payment__isnull=True)

class Cart(models.Model):
    propicker = models.ForeignKey('propicker.Propicker', on_delete=models.CASCADE)
    create_date = models.DateTimeField('생성일', auto_now_add=True)
    payment = models.OneToOneField('Payment', on_delete=models.CASCADE, null=True, blank=True,
                                   default=None, related_name="pay_check")
    # total_price = models.PositiveIntegerField('cart_total_price')

    cart = CartManager()
    
    class Meta:
        verbose_name = ('cart')
        verbose_name_plural = ('carts')
        ordering = ('pk',)

    def __str__(self):
        return '{}'.format(self.pk)

    
class PhotoManager(models.Manager):
    def get_photos(self, cart_id):
        return self.get_queryset().filter(cart = cart_id)

    def set_cart_photos(self, user):
        # 새로운 테이블을 정의 -> django에서 조인하는 방법 
        new_record = self.values(
            'cart__propicker', 'photo', 'photo__name', 'select_quality', 'quality_price'
        ).filter(cart__propicker = user.propicker)

    def get_calculate_photo(self, user):
        return self.get_queryset().filter(photo__user__user = user)

    def get_download_photo(self, user):
        # 결제가 완료된 카트들을 가져온다. 
        pay_carts = Cart.cart.get_cart_show()
        print(pay_carts, "어떻게 들어오는지")
        return self.get_queryset




class PhotoDetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    photo = models.ForeignKey('gallery.Photo', on_delete=models.CASCADE, null=True, related_name='cart_get_photo')
    FREE = "무료화질";
    LOW = '저화질';
    MIDDLE = '중간화질';
    HIGH = '고화질';
    SELECT = (
        (FREE, "무료화질"),
        (LOW, '저화질'),
        (MIDDLE, '중간화질'),
        (HIGH, '고화질')
    )
    select_quality = models.CharField('선택화질', default="무료화질", max_length=10, choices=SELECT, null=True)
    quality_price = models.PositiveIntegerField('화질별 금액', default=0)

    get_object = PhotoManager()

    class Meta:
        verbose_name = ('detail')
        verbose_name_plural = ('details')
        ordering = ('pk',)

    
    def __str__(self):
        return '{}'.format(self.pk)


    def set_price(self, select_quality):
        if select_quality == '무료화질':
            quality_price = 0

        elif select_quality == '저화질':
            quality_price = Photo.price * 0.4

        elif select_quality == '중간화질':
            quality_price = Photo.price * 0.7

        elif select_quality == '고화질':
            quality_price = Photo.price

        return quality_price



