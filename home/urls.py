from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('help/', views.help_page, name='help_page'),
]
