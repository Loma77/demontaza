import os
from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
import shutil

from bands.models import Band


def get_upload_path_news_picture(instance, filename):
    return 'news_picture/{0}/{1}/{2}/'.format(instance.creator.id, instance.id, filename)


class News(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, null=True, blank=True)
    # cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, null=True, blank=True)
    # organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    news = RichTextField(max_length=1000, null=True, blank=True)
    news_picture = models.ImageField(upload_to=get_upload_path_news_picture, null=True, blank=True)
    yt_video = models.CharField(max_length=250, null=True, blank=True)
    fb_event = models.CharField(max_length=250, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created', 'updated', 'creator')
        verbose_name_plural = 'News'

    def __str__(self):
        if self.band:
            return str(self.band.name) + " - " + str(self.title)
        else:
            return str(self.creator.first_name) + " " + str(self.creator.last_name)

    def delete_picture(self):
        self.news_picture.delete()
        dir_path = 'media/news_picture/{0}/{1}/'.format(self.creator.id, self.id)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    def create_news_picture(self):
        dir_path = 'media/news_picture/{0}/{1}/'.format(self.creator.id, self.id)
        os.makedirs(dir_path)
