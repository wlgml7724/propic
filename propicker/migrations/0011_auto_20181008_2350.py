# Generated by Django 2.0.7 on 2018-10-08 14:50

from django.db import migrations, models
import mysite.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('propicker', '0010_auto_20181008_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propicker',
            name='upload',
            field=models.FileField(blank=True, storage=mysite.storage_backends.Public1MediaStorage(), upload_to=''),
        ),
    ]