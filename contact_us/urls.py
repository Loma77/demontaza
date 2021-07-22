from django.urls import path
from . import views

app_name = "contact_us"

urlpatterns = [
    path('', views.help_page, name='help'),
    path('success/', views.help_email_success, name='success'),
    path('account/', views.help_page_account, name='help_account'),
    path('account/success/', views.help_email_success_account, name='account_success'),
]
