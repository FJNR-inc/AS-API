# Generated by Django 2.2.5 on 2019-12-26 16:39

import artsouterrain.apps.user.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', artsouterrain.apps.user.managers.UserManager()),
            ],
        ),
    ]