from django.db import models
from propicker.models import Propicker
from gallery.models import Photo

class Question(models.Model):
     # 질문제목
     question_title = models.CharField('질문제목', max_length=100, unique=True)
     # 질문내용
     question_text = models.TextField('질문내용', max_length = 256)
     # 질문 생성일
     question_create_date = models.DateTimeField('질문작성일', auto_now_add=True)
     # 질문 작성자
     propicker_id = models.ForeignKey(Propicker, on_delete=models.CASCADE)

     class Meta:
          verbose_name='질문'
          verbose_name_plural = '질문모음'
          ordering = ['propicker_id',  ]

     def __str__(self) :
          return '{}({})'.format(self.question_title, self.propicker_id)



class Answer(models.Model):
     # 질문
     question_title = models.ForeignKey(Question, on_delete=models.CASCADE)
     # 답변내용
     answer_text = models.TextField('답변내용', max_length = 256)
     # 답변 작성일
     answer_create_date = models.DateTimeField('답변 작성일', auto_now_add = True)


     class Meta:
          verbose_name='답변'
          verbose_name_plural = '답변모음'
          ordering = ['question_title',  ]

     def __str__(self):
          return '{}'.format(self.question_title)


class Report(models.Model):
     #게시글
     photo = models.CharField('게시물 url', max_length=256)
     #신고자
     reporter = models.ForeignKey(Propicker, on_delete=models.CASCADE)
     #신고자 메일주소
     reporter_email = models.CharField('신고자 메일주소', max_length=100)
     #신고자 번호
     reporter_number = models.CharField('신고자 연락처', max_length=100)
     #신고내용
     report_text = models.TextField('신고내용', max_length = 256)
     #신고파일
     report_file = models.FileField('첨부파일', upload_to='report/', null='True', blank=True)
     #신고유형
     report_type= models.CharField('신고유형', max_length=100)
     # 신고일자
     create_date = models.DateTimeField('신고일자', auto_now_add=True)
     # 신고 처리여부
     NONE = 0
     THREE_MONTH = 1
     ETERNAL = 2
     NOREAD = 3
     PUNISH = (
          (NONE, '징계없음'),
          (THREE_MONTH, '회원 정지 3개월'),
          (ETERNAL , '회원 영구 정지'),
          (NOREAD, '미확인'),
     )
     #징계여부
     punish = models.IntegerField('징계여부', choices=PUNISH, default=3, blank = True)


     class Meta:
          verbose_name='report'
          verbose_name_plural = 'reports'
          ordering = ['create_date',  'reporter', ]

     def __str__(self):
          return '{}{}'.format(self.photo, self.create_date)



