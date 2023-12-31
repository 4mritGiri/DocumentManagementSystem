# Generated by Django 5.0 on 2023-12-31 05:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmsApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='document',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='document',
            name='file_path',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='package',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='package',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
