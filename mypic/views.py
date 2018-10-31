from django.views.generic import ListView, DetailView
from theme.models import *
from calculate.views import *
from gallery.models import *
from propicker.models import *
from django.shortcuts import redirect
# from theme.forms import PhotoInlineFormSet
from itertools import chain
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from mysite.views import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class MypicLV(LoginRequiredMixin, ListView):
	

	def get(self, request, *args, **kwargs):
		gallery =  Photo.objects.filter(user=self.request.user.propicker)
		like = Like.objects.filter(user=self.request.user)
		calculate = Calculate.get_cart(request.user)
		accounts = UserAccount.objects.filter(user = self.request.user.propicker)
		propickers = Propicker.objects.filter(user = self.request.user)
		carts = PhotoDetail.get_object.get_download_photo(request.user)
		user_like = UserLike.objects.filter(like_user=self.request.user.propicker)
		return render(request, 'mypic/mypic_all.html',
			{'gallery': gallery, 'like': like, 'calculate' : calculate, 'accounts' : accounts, 'propickers': propickers, 'carts': carts, 'user_like':user_like})

