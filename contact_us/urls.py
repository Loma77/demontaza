from django.urls import path
from . import views

app_name = "contact_us"

urlpatterns = [
    path('', views.help_page, name='help'),
    path('success/', views.help_email_success, name='success'),
]
