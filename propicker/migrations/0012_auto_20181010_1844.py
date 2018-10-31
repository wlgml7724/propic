# Generated by Django 2.0.5 on 2018-10-10 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propicker', '0011_auto_20181008_2350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='propicker',
            options={'ordering': ['pk'], 'verbose_name': 'propicker', 'verbose_name_plural': 'propickers'},
        ),
        migrations.RemoveField(
            model_name='propicker',
            name='email_confirmed',
        ),
        migrations.AlterField(
            model_name='propicker',
            name='user_state',
            field=models.CharField(choices=[('no', '일반'), ('pa', '일시정지'), ('st', '영구정지'), ('qu', '탈퇴')], default='no', max_length=2, verbose_name='회원상태'),
        ),
    ]