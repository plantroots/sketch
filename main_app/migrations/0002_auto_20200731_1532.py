# Generated by Django 3.0.8 on 2020-07-31 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='notes_str',
            new_name='notes',
        ),
    ]
