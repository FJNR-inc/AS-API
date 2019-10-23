# Generated by Django 2.2.5 on 2019-10-23 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artwork', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Last name')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name='Country')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Picture')),
            ],
        ),
        migrations.CreateModel(
            name='ArtworkType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Artwork Type')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Place Name')),
            ],
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Picture')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artworks', to='artwork.Artist', verbose_name='artist')),
                ('artwork_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artworks', to='artwork.ArtworkType', verbose_name='Artwork Type')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artworks', to='artwork.Place', verbose_name='Place')),
            ],
        ),
    ]