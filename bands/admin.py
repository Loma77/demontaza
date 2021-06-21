from django.contrib import admin
from .models import Genre, Band


admin.site.register(Genre)


class AdminsInline(admin.TabularInline):
    model = Band.admins.through
    extra = 1
    verbose_name = 'Admin'
    verbose_name_plural = 'Admins'


class BandFollowersInline(admin.TabularInline):
    model = Band.users_follow.through
    extra = 1
    verbose_name = 'Band Follower'
    verbose_name_plural = 'Band Followers'


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'city_or_town', 'year_of_creation', 'activity', 'created', 'updated')
    list_filter = ('genre', 'city_or_town', 'year_of_creation', 'activity', 'created', 'updated')
    ordering = ('created', 'activity')
    inlines = [AdminsInline, BandFollowersInline]
    exclude = ('admins', 'users_follow')
