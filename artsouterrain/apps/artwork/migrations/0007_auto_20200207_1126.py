# Generated by Django 2.2.5 on 2020-02-07 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artwork', '0006_updatedata_places_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='updatedata',
            name='artists_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='updatedata',
            name='artwork_types_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='updatedata',
            name='artworks_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
