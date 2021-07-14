import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import shutil


def get_upload_path_logo(instance, filename):
    return 'logo/{0}/{1}/{2}/'.format(instance.creator.id, instance.id, filename)


def get_upload_path_band_picture(instance, filename):
    return 'band_picture/{0}/{1}/{2}/'.format(instance.creator.id, instance.id, filename)


class Genre(models.Model):
    genre = models.CharField(max_length=50)
    main_genre = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.genre)


class Location(models.Model):
    place = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True, default="Serbia")

    def __str__(self):
        return str(self.place)


class Band(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    admins = models.ManyToManyField(User, related_name='band_admins', blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    logo = models.ImageField(upload_to=get_upload_path_logo, null=True, blank=True)
    band_picture = models.ImageField(upload_to=get_upload_path_band_picture, null=True, blank=True)
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)
    city_or_town = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    year_of_creation = models.IntegerField(null=True, blank=True,
                                           help_text="<br>* Molimo vas unesite samo godinu osnivanja radi pravilnog"
                                                     " upisa.")
    members = RichTextField(max_length=1000, null=True, blank=True,
                            help_text="<br>* Molimo vas unesite samo imena članova benda u ovo polje.")
    bio = RichTextField(max_length=2000, null=True, blank=True)
    activity = models.BooleanField(default=False)
    yt_video1 = models.CharField(max_length=250, null=True, blank=True)
    yt_video2 = models.CharField(max_length=250, null=True, blank=True)
    yt_video3 = models.CharField(max_length=250, null=True, blank=True)
    youtube = models.CharField(max_length=250, null=True, blank=True)
    facebook = models.CharField(max_length=250, null=True, blank=True)
    soundcloud = models.CharField(max_length=250, null=True, blank=True)
    instagram = models.CharField(max_length=250, null=True, blank=True)
    band_camp = models.CharField(max_length=250, null=True, blank=True)
    users_follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='band_follows', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', 'created', 'updated')

    def __str__(self):
        return str(self.name)

    def delete_logo(self):
        dir_path = 'media/logo/{0}/{1}/'.format(self.creator.id, self.id)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    def delete_picture(self):
        dir_path = 'media/band_picture/{0}/{1}/'.format(self.creator.id, self.id)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    def create_logo(self):
        dir_path = 'media/logo/{0}/{1}/'.format(self.creator.id, self.id)
        os.makedirs(dir_path)

    def create_picture(self):
        dir_path = 'media/band_picture/{0}/{1}/'.format(self.creator.id, self.id)
        os.makedirs(dir_path)
