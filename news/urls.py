from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('create/user/', views.user_create_news, name='user_create_news'),
    path('create/band/<int:band_id>/', views.band_create_news, name='band_create_news'),
    path('edit/user/<int:news_id>/', views.user_edit_news, name='user_edit_news'),
    path('edit/band/<int:band_id>/<int:news_id>/', views.band_edit_news, name='band_edit_news'),
    path('display/<int:news_id>/', views.news_display_page, name='news_display'),
]
