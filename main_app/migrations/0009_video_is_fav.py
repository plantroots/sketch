# Generated by Django 3.0.8 on 2020-08-09 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_auto_20200809_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='is_fav',
            field=models.BooleanField(default=False),
        ),
    ]
