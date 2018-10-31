from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from mysite.storage_backends import *
from django import forms

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(label = '성')
	last_name = forms.CharField(label = '이름')
	username = forms.CharField(label = '아이디')
	password1 = forms.CharField(label = '비밀번호', widget=forms.PasswordInput)
	password2 = forms.CharField(label = "비밀번호 재확인", widget=forms.PasswordInput)
	birth = forms.DateField()
	phone = forms.CharField(label='핸드폰 번호',help_text='A valid email address, please.')
	isMale = forms.BooleanField(label='성별', 
        required=False,
        initial=False,help_text='남자인 경우 체크해주세요!')
	email = forms.EmailField(label='이메일')
	# name = forms.CharField()
	
	class Meta:
		model = User
		fields = ['username', 'isMale', 'first_name', 
            'last_name', 'birth', 'password1', 'password2', 'phone', 'email']

class IDSearchForm(forms.Form):
    search_word = forms.CharField(label='이름')
    search_word2 = forms.CharField(label='전화번호')

class PWSearchForm(forms.Form):
    search_word = forms.CharField(label='아이디')
    search_word2 = forms.CharField(label='이름')
    search_word3 = forms.CharField(label='전화번호')


class ProfileForm(forms.ModelForm):
	
	
	class Meta:
		model = Propicker
		fields = ('upload', 'content', 'phone', 'birth')





class UserForm(forms.ModelForm):	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username','email')



