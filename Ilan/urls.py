from django.contrib import admin
from django.urls import path, include
from . import views

# Url adresleri ve yönlendirilecekleri views.py üzerindeki fonksiyonlar
urlpatterns = [
    path('', views.index, name = "index"),
    path('create-ilan/', views.create, name = "create-ilan"),
    path('ilan-list/', views.ilan, name = "ilan-list"),
    path('detail/<int:id>', views.detail, name = "detail"),
]