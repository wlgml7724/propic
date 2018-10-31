from django import forms
from gallery.models import *
class GallerySearchForm(forms.Form):
    search_word = forms.CharField(label='Search')


	