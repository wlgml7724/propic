# Generated by Django 2.0.7 on 2018-10-30 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_remove_cart_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='merchant_uid',
            field=models.CharField(default=0, max_length=30, verbose_name='고유주문번호'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(max_length=20, verbose_name='결제방식'),
        ),
    ]
