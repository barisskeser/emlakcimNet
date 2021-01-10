from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.create, name = "create-tahmin"),
    path('show/<int:id>', views.show, name = "show-tahmin"),
    path('register/<int:id>', views.register, name = "register-tahmin"),
]