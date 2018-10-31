from django import forms

from .models import Report

class QnaSearchForm(forms.Form):
    search_word = forms.CharField(label='Search')



class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ('reporter', 'reporter_email','report_text', 'report_file')