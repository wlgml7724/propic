# Generated by Django 2.0.5 on 2018-10-06 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propicker', '0005_remove_propicker_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='propicker',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
