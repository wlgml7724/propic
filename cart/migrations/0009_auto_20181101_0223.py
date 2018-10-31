# Generated by Django 2.0.7 on 2018-11-01 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_auto_20181031_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photodetail',
            name='select_quality',
            field=models.CharField(choices=[('무료화질', '무료화질'), ('저화질', '저화질'), ('중간화질', '중간화질'), ('고화질', '고화질')], default='무료화질', max_length=10, null=True, verbose_name='선택화질'),
        ),
    ]
