# Generated by Django 2.0.7 on 2018-10-08 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propicker', '0007_useraccount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='propicker_id',
            new_name='user',
        ),
    ]