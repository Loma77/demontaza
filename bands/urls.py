from django.urls import path, re_path
from . import views

app_name = 'bands'

urlpatterns = [
    path('search/all/', views.band_search_page, name='search_page'),
    path('page/<int:band_id>/', views.band_page, name='band_page'),
    # Account band pages
    path('account/search/all/', views.account_band_search_page, name='account_search_page'),
    path('account/create-page/', views.account_create_band_page, name='band_create_page'),
    path('account/page/<int:band_id>/', views.account_band_page, name='account_band_page'),
    path('account/edit-page/<int:band_id>/', views.account_band_edit_page, name='band_edit_page'),
    path('account/admins/<int:band_id>/', views.account_band_admins_page, name='band_admin_page'),
]
