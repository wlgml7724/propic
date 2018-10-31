from django.conf.urls import url

from qna.views import *
app_name='qna'
urlpatterns = [

  # Example: /
    url(r'^$', QnaLV.as_view(), name='index'),

    url(r'^qna/(?P<pk>\d+)/$', QnaDV.as_view(), name='qna'),

    url(r'^report/$', ReportLV.as_view(), name='report'),

    url(r'^report/check/$', CheckLV.as_view(), name='check'),

    url(r'^report/copyright/$', CopyCreateView.as_view(), name='copyright'),

    url(r'^report/slash/$', SlashCreateView.as_view(), name='slash'),
]