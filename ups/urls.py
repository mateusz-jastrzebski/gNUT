# pages/urls.py

from django.urls import path
from ups import views

app_name = 'ups'

urlpatterns = [
    path("", views.home, name='home'),
    path("get_ups_list/", views.get_ups_list, name='get_ups_list'),
    path('<str:ups>/', views.ups_view, name='ups_view'),
]
