from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView

##from django.contrib.auth.forms import UserCreationForm
##from mysite.forms import MySiteSignUp
from propicker.forms import *
from gallery.models import Photo
from theme.models import Theme
from django import forms
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import *
from django.contrib.auth.models import User

# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.propicker.birth = form.cleaned_data.get('birth')
            user.propicker.phone =form.cleaned_data.get('phone')
            user.propicker.isMale = form.cleaned_data.get('isMale')
            # print(password1)
            user.save()
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})



    

#--- TemplateView
class HomeView(ListView):
    model = Photo
    def get(self, request, *args, **kwargs):
        gallery =  Photo.objects.all();
        propickers = Propicker.objects.all();
        theme = Theme.objects.all();
        return render(request, 'home.html',
            {'gallery': gallery,'propickers': propickers, 'theme':theme})


    template_name = 'home.html'

#--- User Creation
# 회원가입 약관동의 
class UserCreateBefore(TemplateView):
    template_name = 'registration/register_before.html'

# 회원가입    
class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    # form_class = SignUp
    success_url = reverse_lazy('register_done')

# 회원가입 완료 
class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'


### 회원정보 수정_비밀번호 확인 
##class UserPasswordCheck(PasswordChangeView):
##    form_class = PasswordCheckForm
##    template_name = 'registration/register_change_before.html'
##    success_url = reverse_lazy('password_change_done')
##
### 회원정보 수정
##class UserChangeView(CreateView):
##    template_name = 'registration/register_change.html'
##    form_class = RegisterUpdateForm
##    success_url = reverse_lazy('home')
    
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
        
##class UserUpdateView(UpdateView):
##    model = User
##    fields = ['image','photo_name','img_content', 'price','tag']
##    success_url = reverse_lazy('gallery:index')


