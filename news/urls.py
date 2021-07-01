from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('create/user/', views.user_create_news, name='user_create_news'),
]
