from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from cart.models import *
from django.core.handlers.wsgi import WSGIRequest
from mysite import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import AbstractUser
from cart.Cart_Object import *
from propicker import *
from calculate import *
from django.urls import reverse_lazy
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import *
User = get_user_model()


class ChartView(View):
    def get(self, request, *args, **kwargs):
        chart_list =  Calculate.get_cart(request.user).filter(cart__create_date__year = 2018)
        accounts = UserAccount.objects.all()
        return render(request, 'charts.html', {'accounts': accounts, 'chart_list': chart_list})


def get_data(request, *args, **kwargs):
    photos = Calculate.get_cart(request.user)
    data = {
		"sales": 20,
		"customers": 10,
	}
    print(request.user)
    return JsonResponse(data) # http response


class ChartData(APIView):
	# 차트 생성해주는 api
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        photos = Calculate.get_cart(request.user)
        labels=["1월","2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
        default_items = []

        for i in range(1, 12):
            search = request.GET.get('year')
            p = photos.filter(cart__create_date__month = i) and photos.filter(cart__create_date__year=search)
            # print(p)
            if p is None:
                k = 0
            else:
                k = Cart_Object.sum_price2(p)
            default_items.append(k)

        data = {
        # "photo" : photo,
        "labels": labels,
        "default": default_items,

        }
        return Response(data)

@login_required
class Calculate:
	def get_cart(param_user):
		if False:
			print("유저없음")
		else:		
			return Cart.cart.exclude(payment__isnull=True) and PhotoDetail.get_object.get_calculate_photo(param_user)
