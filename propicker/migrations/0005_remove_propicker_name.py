# Generated by Django 2.0.5 on 2018-10-06 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propicker', '0004_auto_20181007_0156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propicker',
            name='name',
        ),
    ]
