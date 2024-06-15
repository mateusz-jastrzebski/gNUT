# pages/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path("login/", views.login_view, name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
