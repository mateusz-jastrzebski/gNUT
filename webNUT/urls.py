"""
URL configuration for webNUT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.ups, name='ups')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='ups')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from ups.views import page_not_found, unauthorized

urlpatterns = [
    path('auth/', include("authentication.urls")),
    path('config/', include("configuration.urls")),
    path('', include("ups.urls")),
]

urlpatterns += [re_path(r'^.*/$', page_not_found)]
urlpatterns += [re_path(r'^.*/$', unauthorized)]
