# Generated by Django 3.0.8 on 2020-08-09 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20200805_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Video')),
            ],
        ),
    ]
