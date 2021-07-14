from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import os
import shutil

from bands.models import Genre


def get_upload_path(instance, filename):
    return 'profile_photos/{0}/{1}/'.format(instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    last_time_login = models.DateTimeField(default=timezone.now)
    friends = models.ManyToManyField(User, related_name='user_friends', blank=True)
    interests = models.ManyToManyField(Genre, related_name='user_interests', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

    def delete_picture_path(self):
        dir_path = 'media/profile_photos/{0}/'.format(self.user.username)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    def create(self):
        dir_path = 'media/profile_photos/{0}/'.format(self.user.username)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
