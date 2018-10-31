from gallery.models import Photo
from propicker.models import Propicker
from cart.models import Cart, PhotoDetail, Payment
from django.views.generic import (
	ListView, DetailView, TemplateView, View, CreateView, UpdateView, DeleteView
)
import datetime

from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import User
from mysite.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse

import json
from django.http import JsonResponse
from cart.Cart_Object import Cart_Object

class PG(View, LoginRequiredMixin):
	model : PhotoDetail
	template_name = "cart/PG.html"

	# def save_pg_payment(self):



# 181004_16:30주석 
@login_required
def detail(request): #, Cart_Object):
	get_user_cart = False
	set_new_cart = False
	remove_photo = False

	# 카트에 이미지를 삭제가 상단에 있어야함, 추가, 수정은 gallery_view에서 진행
	if remove_photo:
		pass
	# 카트가 존재하는지 확인한다. 
	if Cart.cart.get_cart().count():
		# 데이터 베이스에 카트가 존재할 때
		get_user_cart = True
		print("카트존재, 개수", Cart.cart.get_cart().count())
	else:
		set_new_cart = True

	# 카트가 존재하지 않으면 카트를 생성
	if set_new_cart:
		print("request", request)
		print("request.user", request.user)
		cart = Cart_Object.new(Cart, request)
		print("새로만들어진 카트번호", cart)
		return render(request, 'cart/cartDetail.html')


	# 카트와 카트의 상품을 가져온다. 
	if get_user_cart:
		# 현재 로그인 된 
		cart = Cart.cart.get_cart().get(propicker_id = request.user.propicker)
		detail = PhotoDetail.get_object.get_photos(cart)
		sum_price = Cart_Object.sum_price(request, detail)
		context = {
			'cart':cart, 
			'detail': detail, 
			'sum_price': sum_price
		}
		print("가져오는 카트", cart)
		print("가져오는 카트 사진", detail)
		print("sum_price", sum_price)
		return render(request, 'cart/cartDetail.html', context)


class photoDelete(LoginRequiredMixin, DeleteView):
    model = PhotoDetail
    success_url = reverse_lazy('cart:detail')



@login_required
@require_POST
def add_cart_payment(request):
    cart = request.POST.get('cart', None)
    merchant_uid = request.POST.get('merchant_uid', None)
    pay_method = request.POST.get('pay_method', None)
    price = request.POST.get('price', 0)
    # 새로운 결제 추가 
    print("json파일 넘어오기까지 완료")
    payment = Download.save_payment(photo_pk, merchant_uid, pay_method, price)
    # 새로운 카트 생성, cart는 새로운 카트 번호
    print("payment값 생성", payment)
    cart = Download.save_cart(request, payment)
    print("cart생성", cart)

    try:
        print("try작동")
        # 장바구니에 담겨져 있는 데이터인지 확인하기
        detail = PhotoDetail.get_object.filter(
            photo=photo,
            cart__propicker = request.user.propicker,
        )
        print("try의 detail", detail)
    except:
        # 장바구니에 데이터가 들어있지 않으면 그냥 카트 생성 후 저장
        # 데이터 저장
        print("except실행")
        detail = PhotoDetail()
        detail.cart = cart
        detail.photo = photo
        detail.save()
        # 카트에 결제내역 저장
        cart.save() 
    else:
        print("else실행")
        # 장바구니에 데이터가 들어있으면 장바구니에서 삭제하고 새로운 장바구니에 추가 후에 결제정보 저장
        detail = PhotoDetail()
        detail.photo = photo
        detail.cart = cart
        detail.save()
        # 카트에 결제내역 저장
        print("최종 이미지", detail)

    context = {'detail_pk': detail.pk}

    return HttpResponse(json.dumps(context))


def get_download_photos(request):
	print("get_down_photo 작동")
	carts = PhotoDetail.get_object.get_download_photo(request.user)
	print("get_down_photo 작동결과", carts)
	car = list(carts())
	# carts는 QuerySet으로 cart 객체들이 들어오고 

	context = {'carts' : carts() }
	# carts()를 출력하면 photoDetail값들이 출력된다. -> 어떻게 리스트로 가져오지...

	return render(request, 'gallery/download.html', context)
