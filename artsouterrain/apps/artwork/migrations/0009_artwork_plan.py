# Generated by Django 2.2.5 on 2020-02-08 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artwork', '0008_auto_20200208_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='plan',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Plan'),
        ),
    ]