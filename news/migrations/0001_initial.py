# Generated by Django 3.0.14 on 2021-06-25 09:26

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import news.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bands', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('news', ckeditor.fields.RichTextField(blank=True, max_length=1000, null=True)),
                ('news_picture', models.ImageField(blank=True, null=True, upload_to=news.models.get_upload_path_news_picture)),
                ('yt_video', models.CharField(blank=True, max_length=250, null=True)),
                ('fb_event', models.CharField(blank=True, max_length=250, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('band', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bands.Band')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'News',
                'ordering': ('created', 'updated', 'creator'),
            },
        ),
    ]