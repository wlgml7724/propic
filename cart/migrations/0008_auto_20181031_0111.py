# Generated by Django 2.0.7 on 2018-10-31 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_auto_20181030_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='merchant_uid',
            field=models.CharField(blank=True, default=None, max_length=30, null=True, verbose_name='고유주문번호'),
        ),
    ]
