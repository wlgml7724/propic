# Generated by Django 2.0.7 on 2018-10-04 06:45

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('propicker', '0001_initial'),
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
                'ordering': ('pk',),
            },
            managers=[
                ('cart', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='결제일자')),
                ('method', models.IntegerField(choices=[(0, '신용카드'), (1, '국민은행 가상계좌'), (2, '우리은행 가상계좌')], default=0, verbose_name='결제방식')),
                ('price', models.IntegerField(verbose_name='결제금액')),
            ],
            options={
                'verbose_name': 'payment',
                'verbose_name_plural': 'payments',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='PhotoDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('select_quality', models.CharField(choices=[('무료화질', '무료화질'), ('저화질', '저화질'), ('중간화질', '중간화질'), ('고화질', '고화질')], default='무료화질', max_length=10, verbose_name='선택화질')),
                ('quality_price', models.IntegerField(default=0, verbose_name='화질별 금액')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.Cart')),
                ('photo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_get_photo', to='gallery.Photo')),
            ],
            options={
                'verbose_name': 'photo_detail',
                'verbose_name_plural': 'photo_details',
                'ordering': ('pk',),
            },
            managers=[
                ('get_object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='payment',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pay_check', to='cart.Payment'),
        ),
        migrations.AddField(
            model_name='cart',
            name='propicker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='propicker.Propicker'),
        ),
    ]