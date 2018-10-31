from .models import Cart, PhotoDetail, Payment
from gallery.models import *
import datetime


class Cart_Object:
	# print("\n\nCart_Object시작")
	def __init__(self):
		self.cart = 0
		if Cart.cart.get_cart().count():
			# 불러오는 카트가 1개이상 존재할 떄 
			try:
				cart = Cart.cart.get_cart().get_object_or_404(propicker_id = request.user.propicker)
			except models.Cart.DoesNotExist:
				cart = self.new(request)
				print("create_new_cart", cart)
		else: 
			print("새카르틑 생성함")
			cart = self.new(request)
		# 여기서 카트를 설정해준다. -> 
		self.cart = cart
		return cart

	def sum_price2(detail):
		total = 0
		for item in detail:
			total += item.quality_price
		return total

	@classmethod
	# 카트가 존재하지 않을 경우 새로 생성
	def set_cart(cls, request):
		cart = Cart.cart.get_cart(propicker_id = request.user.propicker)
		return cart

	def new(cls, request):
		new_cart = Cart(
			create_date = datetime.datetime.now(),
			propicker = request.user.propicker
		)
		new_cart.save()
		return new_cart

	def sum_price(cls, detail):
		total = 0
		for item in detail:
			total += item.quality_price
		return total

	def change(cls, detail, select_quality, quality_price):
		print("change함수 실행")
		detail.select_quality = select_quality
		print('저장하는거', detail.select_quality)
		detail.quality_price = quality_price
		print('저장하는거', detail.quality_price)
		detail.save()


	def cart_add(request):
	    photo_pk = request.POST.get('pk', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
	    photo = get_object_or_404(Photo, pk=photo_pk)
	    cart = Cart.cart.get_cart().get(propicker_id = request.user.propicker)
	    select_quality = request.POST.get('select_quality')
	    quality_price = request.POST.get('quality_price')
	    
	    try:
	        print("try시작")
	        # 현재 카트에 이미지가 들어있는 경우 
	        detail = PhotoDetail.get_object.get(
	            cart=cart,
	            photo=photo,
	        )
	        print("def add_try", detail)
	    except PhotoDetail.DoesNotExist:
	        print("photonotexist")
	        detail = PhotoDetail()
	        detail.cart = cart
	        detail.photo = photo
	        detail.select_quality = select_quality
	        detail.quality_price = quality_price
	        detail.save()
	    else:
	        Cart_Object.change(request, detail, select_quality, quality_price)

	    context = {'detail.select_quality': detail.select_quality}

	    return HttpResponse(json.dumps(context))



class Download:
	def get_download(user):
		return None

	def save_payment(photo_pk, merchant_uid, pay_method, price):
		# 새로운 결제추가
		new_payment = Payment(
			method=pay_method, 
	        price=price,
	        merchant_uid=merchant_uid
		)
		new_payment.save()
		return new_payment

	def save_cart_payment():
		return new_payment

	def save_cart(request, payment_pk):
		new_cart = Cart(
			create_date = datetime.datetime.now(),
			propicker = request.user.propicker,
			payment = payment_pk
		)
		new_cart.save()
		return new_cart