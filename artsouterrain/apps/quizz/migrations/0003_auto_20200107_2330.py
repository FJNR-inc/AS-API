# Generated by Django 2.2.5 on 2020-01-07 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizz', '0002_auto_20191211_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='user',
        ),
        migrations.AddField(
            model_name='submission',
            name='email',
            field=models.CharField(default=None, max_length=255, verbose_name='Participant email'),
            preserve_default=False,
        ),
    ]