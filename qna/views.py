from django.views.generic import ListView, DetailView
from theme.models import *
from gallery.models import *
from qna.models import *
from django.shortcuts import redirect
from qna.forms import QnaSearchForm
from django.views.generic.edit import FormView
# from theme.forms import PhotoInlineFormSet
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from mysite.views import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
class QnaLV(ListView):
    model = Answer
    template_name='FAQ.html'
    context_object_name='qna'
    # paginate_by = 10

#--- DetailView
class QnaDV(DetailView):
    model = Answer
   

class QnaSearchFormView(FormView):
    form_class = QnaSearchForm
    template_name = 'FAQ.html' #자기 자신으로 들어오게 하고 싶음

    def form_valid(self, form) :
        qna_schWord = '%s' % self.request.POST['qna_search_word']
        qna_list = Photo.objects.filter(Q(faq_type__icontains=qna_schWord) | Q(question_title__icontains=qna_schWord) | Q(question_text__icontains=qna_schWord)).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = qna_schWord
        context['object_list'] = qna_list

        return render(self.request, self.template_name, context)



class ReportLV(LoginRequiredMixin,TemplateView):
    template_name='report_before.html'

def report_select(request):
    photo_pk = request.POST.get('pk', None)

    context = {'photo': photo_pk}

    return render(request, 'qna/report_before.html')



class CheckLV(ListView):
    model = Answer
    template_name='report_check_user.html'
    # photo = get_object_or_404(Photo, pk=pk)
    # print(photo)

#--- Create 
class CopyCreateView(LoginRequiredMixin,CreateView):
    model = Report
    template_name='dec_porn.html'
    fields = ['photo','report_text', 'report_file']
    success_url = reverse_lazy('qna:index')


    def form_valid(self, form):
        full_name= User.get_full_name(self.request.user)
        phone = self.request.user.propicker.phone
        print(phone)
        form.instance.reporter = self.request.user.propicker
        form.instance.reporter_email = self.request.user.email
        form.instance.reporter_number = self.request.user.propicker.phone
        form.instance.report_type = '저작권'
        return super(CopyCreateView, self).form_valid(form)

class SlashCreateView(LoginRequiredMixin, CreateView):
    model = Report
    template_name='dec_porn.html'
    fields = ['photo','report_text']
    success_url = reverse_lazy('qna:index')

    def form_valid(self, form):
        form.instance.reporter = self.request.user.propicker
        form.instance.reporter_email = self.request.user.email
        form.instance.reporter_number = self.request.user.propicker.phone
        form.instance.report_type = '음란물'

        return super(SlashCreateView, self).form_valid(form)

