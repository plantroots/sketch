# Generated by Django 3.1 on 2020-08-18 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0020_song_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='length',
        ),
    ]
