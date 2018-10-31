import json
# 다운로드를 위한 import2개 
import urllib.request

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from hitcount.views import HitCountDetailView
from django.shortcuts import render

from gallery.models import *
from tagging.models import Tag, TaggedItem
from tagging.views import TaggedObjectList
from gallery.forms import GallerySearchForm
from mysite.views import LoginRequiredMixin
from propicker.models import Propicker
from cart.Cart_Object import Cart_Object
from cart.models import Payment, Cart, PhotoDetail

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from django.http import JsonResponse

#--- TemplateView
class TagTV(TemplateView) :
    template_name = 'tagging/tagging_cloud.html'

class GalleryTOL(TaggedObjectList) :
    model = Photo
    template_name = 'tagging/tagging_post_list.html'

# Create your views here.
#--- ListView
class GalleryLV(ListView):
    model = Photo
    template_name = 'gallery/gallery_all.html'
    context_object_name = 'gallery'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-pk')
        return ordering



def downloader(request):
    # JSG확장자명으로 다운받기 -> 근데 그러면 오류가 없으려나...
    print("downloader까지 넘어옴")
    image_url = request.GET.get('image_url', None)
    print("url", image_url)
    image_name = request.GET.get('name', None)
    print("imagename", image_name)
    full_file_name = str(image_name) + '.jpg'
    print("jpg파일로 만들어짐")
    print(full_file_name) # 이름.jpg
    print("리턴값 출력", urllib.request.urlretrieve(image_url,full_file_name))
    response_tuple = urllib.request.urlretrieve(image_url,full_file_name)

    # response_tupels = [('content-length', '2501479'), ('accept-ranges', 'bytes'),]
    # response = dict(response_tupels)
    # try:
    #   content_length = int(response['content-length'])
    # context = {'detail.select_quality': detail.select_quality}

    return HttpResponse(json.dumps(context))





#--- DetailView
class GalleryDV(HitCountDetailView):
    model = Photo
    count_hit = True 
    def get_context_data(self, *args, **kwargs):
        queryset = Photo.objects.filter(uploaded_at__year=2018)
        context = super(GalleryDV, self).get_context_data(*args, **kwargs)
        context['photo_list'] = queryset.random(4)
        return context
    

#--- Create / Update / Change / Delete
class GalleryCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['img','name','content', 'price','tag', 'genre',]
    success_url = reverse_lazy('gallery:change')

    def form_valid(self, form):  
        # self.object = form.save(commit=False)      
        form.instance.user = self.request.user and self.request.user.propicker
        return super(GalleryCreateView, self).form_valid(form)


class GalleryChangeLV(LoginRequiredMixin, ListView):
    template_name = 'gallery/gallery_change_list.html'
    

    def get_queryset(self): 
        return Photo.objects.filter(user__user=self.request.user)

class GalleryUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['img','name','content', 'price','tag', 'genre',]
    success_url = reverse_lazy('gallery:change')

class GalleryDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('gallery:change')


#--- FormView
class SearchFormView(FormView):
    form_class = GallerySearchForm
    template_name = 'gallery/photo_search.html'

    def form_valid(self, form) :
        schWord = '%s' % self.request.POST['search_word']
        photo_list = Photo.objects.filter(Q(name__icontains=schWord) | Q(tag__icontains=schWord) | Q(content__icontains=schWord)).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = schWord
        context['object_list'] = photo_list

        return render(self.request, self.template_name, context)


@login_required
@require_POST
def photo_like(request):
    pk = request.POST.get('pk', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
    photo = get_object_or_404(Photo, pk=pk)
    photo_like, photo_like_created = photo.like_set.get_or_create(user=request.user)

    if not photo_like_created:
        photo_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"

    context = {'like_count': photo.like_count,
               'message': message,
               'nickname': request.user.username }

    return HttpResponse(json.dumps(context))
    # context를 json 타입으로


#--- ListView
class GalleryLikeLV(ListView):
    model = Like

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

@login_required
@require_POST
def cart_add(request):
    # return Cart_Object.cart_add(request)
    photo_pk = request.POST.get('pk', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
    photo = get_object_or_404(Photo, pk=photo_pk)
    cart = Cart.cart.get_cart().get(propicker_id = request.user.propicker)
    select_quality = request.POST.get('select_quality')
    quality_price = request.POST.get('quality_price')
    try:
        print("try까지는 들어옴", quality_price)
        # 현재 카트에 이미지가 들어있는 경우 
        detail = PhotoDetail.get_object.get(
            cart=cart,
            photo=photo,
        )
        print("def add_try", detail)
    except PhotoDetail.DoesNotExist:
        detail = PhotoDetail()
        detail.cart = cart
        detail.photo = photo
        detail.select_quality = select_quality
        detail.quality_price = quality_price
        detail.save()
    else: #ItemAlreadyExists
        # 새로운 화질을 선택해서 넣으면 그 화질로 변경된다 (change의 개념)
        print("add_cart_else실행", quality_price)
        detail.select_quality = select_quality
        detail.quality_price = quality_price
        detail.save()

    context = {'detail.select_quality': detail.select_quality}

    return HttpResponse(json.dumps(context))

# 상품하나를 바로 결제할 때
# 새로운 카트를 만들어서 저장하는 방식으로 진행
# 이미 결제가 되어있는지 확인 -> 결제가 안되어있으면 결제
@login_required
@require_POST
def add_photo_payment(request):
    photo_pk = request.POST.get('pk', None)
    photo = get_object_or_404(Photo, pk=photo_pk)
    merchant_uid = request.POST.get('merchant_uid', None)
    pay_method = request.POST.get('pay_method', None)
    price = request.POST.get('price', None)
    # 결제내역 저장
    #payment객체 생성
    new_payment = Payment.objects.create(
        method=pay_method, 
        price=price,
        merchant_uid=merchant_uid,
        # photo=Photo.objects.get(pk = photo_pk)
    )
    # new_payment = Payment.save_payment(Payment, pay_method, price, merchant_uid)
    # 새로운 카트 생성, cart는 새로운 카트 번호
    cart = Cart_Object.new(Cart, request)
    '''
    현재 여기 위에까지는 완료, cart는 pk를 의미하는거니까 카트객체를 가져와주어야 한다. 
    그리고 나서 아래의 로직을 짜주면 되는데 이 부분에 대해서는 download객체를 만들어 주는것이 좋을 것 같다. 
    dwonload객체에서는 카트 생성 및 저장, 그리고 연동이 될 듯 하다. 
    그리고 download값을 가져오는 것 -> 두가지 종류의 값을 모두 가져와야 한다. 
    '''
    Cart = Cart() # 카트객체 생성
    try:
        # 장바구니에 담겨져 있는 데이터인지 확인하기
        detail = PhotoDetail.get_object.filter(
            photo=photo,
            cart__propicker = request.user.propicker,
        )
    except:
        # 장바구니에 데이터가 들어있지 않으면 그냥 카트 생성 후 저장
        # 데이터 저장
        detail = PhotoDetail()
        detail.cart = cart
        detail.photo = photo
        detail.select_quality = select_quality
        detail.quality_price = quality_price
        detail.save()
        # 카트에 결제내역 저장
        cart.payment = new_payment
        cart.save() 
    else:
        # 장바구니에 데이터가 들어있으면 장바구니에서 삭제하고 새로운 장바구니에 추가 후에 결제정보 저장
        # detail.cart = None
        detail.cart = cart
        detail.save()
        # 카트에 결제내역 저장
        cart.payment = new_payment
        cart.save() 

    context = {'cart.payment': cart.payment}

    return HttpResponse(json.dumps(context))


def add_cart_payment(self):
    return None