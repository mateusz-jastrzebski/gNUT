# pages/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from configuration import views

app_name = 'configuration'

urlpatterns = [
    path('upsd/', views.configure_upsd, name='configure_upsd'),
    path('upsmon/', views.configure_upsmon, name='configure_upsmon'),
    path('general/', views.configure_driver_advanced, name='configure_driver_advanced'),
    path('<str:ups>/', views.configure_driver, name='configure_driver'),
]
