# Generated by Django 3.1 on 2020-08-18 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0021_remove_album_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='my_age',
        ),
    ]
