# Generated by Django 2.0.7 on 2018-11-01 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0004_auto_20181101_0247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='punish',
            field=models.IntegerField(blank=True, choices=[(0, '징계없음'), (1, '회원 정지 3개월'), (2, '회원 영구 정지'), (3, '미확인')], default=3, verbose_name='징계여부'),
        ),
    ]
