# Generated by Django 2.0.7 on 2018-11-01 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propicker', '0016_auto_20181029_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propicker',
            name='content',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='회원소개'),
        ),
    ]
