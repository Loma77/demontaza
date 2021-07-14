from django.urls import path, re_path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('forgot_password/', views.forgot_password_page, name='forgot_password_page'),
    path('create/', views.create_account_page, name='create_account_page'),
    path('home/', views.account_home_page, name='account_home'),
    path('profile/<int:user_id>/', views.account_profile_page, name='account_profile'),
    path('settings/', views.account_settings_page, name='account_settings'),
    path('settings/interests/', views.account_interest, name='personal_interests'),

    re_path(r'^search/(?P<name>[-\S\w\s]+)/$', views.account_search_page, name='search_page'),
]
