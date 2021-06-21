from django.contrib import admin
from .models import Profile, Location

admin.site.register(Location)


class FriendsInline(admin.TabularInline):
    model = Profile.friends.through
    extra = 1
    verbose_name = 'Friend'
    verbose_name_plural = 'Friends'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_time_login')
    list_filter = ('last_time_login', )
    ordering = ('last_time_login', )
    inlines = [FriendsInline, ]
    exclude = ('friends', )
