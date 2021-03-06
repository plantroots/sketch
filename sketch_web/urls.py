"""sketch_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('encoder/', views.encoder, name='encoder'),
    path('videos/', include('main_app.urls')),
    path('albums/<int:id>', views.album_focus, name='album_focus'),
    path('favourites/', views.favourites, name='favourites'),
    path('themes/', views.themes, name='themes'),
    path('harmony/', views.harmony, name='harmony'),
    path('songs/', views.songs, name='songs'),
    path('other/', views.other, name='other'),
    path('album_scan/', views.album_scan, name='album_scan')
]
