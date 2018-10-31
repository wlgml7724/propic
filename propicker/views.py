import json
from django.views.generic import *
from .models import *
from calculate.forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from gallery.models import *
from django.contrib.auth.models import User
from mysite.views import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from propicker.forms import *
from qna.models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from gallery.views import *
from gallery.models import Photo
# Create View
class PropickerLV(ListView):
    template_name = 'propicker/propicker_rank.html'
    model = Propicker
    def get_queryset(self):
        return list(set(Propicker.objects.all().order_by('-like_user_set')))

class RankLV(ListView):
     template_name = 'propicker/propicker_rank.html'
     model = Photo
     def get_ordering(self):
        # print(a)
        ordering = self.request.GET.get('ordering', 'like_user_set')
        return ordering

def propicker_detail(request, pk):
    propicker = get_object_or_404(Propicker, pk=pk)
    photo = Photo.objects.filter(user__user = pk)
    like_count = Like.objects.filter(user = pk)
    return render(request, 'propicker/propicker_detail.html', {'propicker': propicker, 'photo': photo, 'like_count':like_count})
         
def save_account_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user and request.user.propicker
            form.save()
            data['form_is_valid'] = True
            accounts = UserAccount.objects.all()

            data['html_account_list'] = render_to_string('propicker/account_list.html', {
                'accounts': accounts
            })
            print(data['html_account_list'])
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def account_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
    else:
        form = BookForm()
    return save_account_form(request, form, 'propicker/account_create.html')

def account_update(request, pk):
    account = get_object_or_404(UserAccount, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=account)
    else:
        form = BookForm(instance=account)
    return save_account_form(request, form, 'propicker/account_update.html')

def account_delete(request, pk):
    account = get_object_or_404(UserAccount, pk=pk)
    data = dict()
    if request.method == 'POST':
        account.delete()
        data['form_is_valid'] = True
        accounts = UserAccount.objects.all()
        data['html_account_list'] = render_to_string('propicker/account_list.html', {
            'accounts': accounts
        })
    else:
        context = {'account': account}
        data['html_form'] = render_to_string('propicker/account_delete.html', context, request=request)
    return JsonResponse(data)



class IDSearchFormView(FormView):
    form_class = IDSearchForm
    template_name = 'propicker/id_search.html'

    def form_valid(self, form) :
        q = '%s' % self.request.POST['search_word']
        w =  '%s' % self.request.POST['search_word2']      
        context = {}
        context['form'] = form
        context['search_term'] = q, w
        try:
            propicker_query = Propicker.objects.get(phone = w)
            user = propicker_query.user
            print(user)
            full_name = User.get_full_name(user)
            full = full_name.replace(" ", "")
            print("전체이름" ,full_name, 'dd', q)
            if q == full:
                photo_list = Propicker.objects.filter(Q(phone__icontains=w))
                context['object_list'] = photo_list
                print(context)
            else:
                context['object_list'] = []
                print(context)
        except:
            context['object_list'] = []
            print(context)        
        return render(self.request, self.template_name, context)

class PWSearchFormView(FormView):
    form_class = PWSearchForm
    template_name = 'propicker/pw_search.html'

    def form_valid(self, form) :
        q = '%s' % self.request.POST['search_word']
        w =  '%s' % self.request.POST['search_word2']
        d = '%s' % self.request.POST['search_word3']

        context = {}
        context['form'] = form
        context['search_term'] = q, w, d
        try:
            propicker_query = Propicker.objects.get(phone = d)
            user = propicker_query.user
            full_name = User.get_full_name(user)
            full = full_name.replace(" ", "")
            if w == full:
                username = User.get_username(user)
                print('아이디',username)
                if q == username:
                    photo_list = Propicker.objects.filter(Q(user__username__icontains = q) & Q(phone__icontains=d))
                    context['object_list'] = photo_list
                    print(context)
                else:
                    context['objects_list'] = []
        except:
            context['object_list'] = []
            print(context)

        return render(self.request, self.template_name, context)

@login_required
@require_POST
def user_like(request):
    pk = request.POST.get('pk', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
    propicker = get_object_or_404(Propicker, pk=pk)
    print("회원", request.user.propicker, propicker, request.user)
    propicker_like, propicker_like_created = propicker.to_propicker.get_or_create(like_user=request.user.propicker)
    # print(propicker_like)
    if not propicker_like_created:
        propicker_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"


    context = {'like_count': propicker.like_count,
               'message': message,
               'nickname': request.user.username }

    return HttpResponse(json.dumps(context))
    # context를 json 타입으로



class SettingView(LoginRequiredMixin,ListView):
    def get(self, request, *args, **kwargs):
        report = Report.objects.filter(reporter = request.user.propicker)
        print("이게 들어온건가",report)
        return render(request,"propicker/setting.html",{"report" : report} )


def save_user_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            users = User.objects.all()

            data['html_user_list'] = render_to_string('propicker/setting.html', {
                'users': users
            })
            data['form_is_valid'] = True
        else:
            print("dafs")
            data['form_is_valid'] = False
    context = {'form': form}
    data['userhtml_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

    

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)    
    if request.method == 'POST':
        form = UserForm(request.POST, instance = user)      

    else:
        form = UserForm( instance = user)
        print(form.instance.pk)

    return save_user_form(request, form, 'propicker/user_update.html')

def save_profile_form(request, form, template_name):
    print("profile_form저장")
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            print('저장', form.save()) # 1-> true
            propickers = Propicker.objects.all()
            print("프로픽컬", propickers)

            data['html_propicker_list'] = render_to_string('mypic/mypic_all.html', {'propickers': propickers})
            # print('데이터', data['html_propicker_list'])
            data['form_is_valid'] = True
        else:
            print("dafs")
            data['form_is_valid'] = False
    context = {'form': form}
    data['propickerhtml_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

    

def profile_update(request, pk):
    print("profile_update시작")
    propicker = get_object_or_404(Propicker.objects.filter(user= request.user), pk=pk)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance = propicker)
        

    else:
        form = ProfileForm( instance = propicker)
        print(form.instance.pk)

    return save_profile_form(request, form, 'propicker/profile_update.html')



# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'propicker/change_password.html', {'form': form})