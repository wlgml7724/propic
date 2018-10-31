from django.views.generic import ListView, DetailView
from theme.models import *
from gallery.models import *
from django.shortcuts import redirect
# from theme.forms import PhotoInlineFormSet

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from mysite.views import LoginRequiredMixin

# Create your views here.


class ThemeLV(ListView):
    model = Theme

class ThemeDV(DetailView):
    model = Theme

class ThemePhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Theme
    fields = ['theme_title', 'theme_img', 'theme_content', 'photo_id']
    success_url = reverse_lazy('theme:index')

    def get_context_data(self, **kwargs):
    	context = super().get_context_data(**kwargs)
    	photos = Theme.objects.all()
    	context[photos[0]] = Theme.objects.filter(photo_id__user__user=self.request.user)
    	return context