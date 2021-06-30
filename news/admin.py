from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('creator', 'band', 'title', 'created', 'updated')
    list_filter = ('created', 'updated')
    ordering = ('created', 'updated')
