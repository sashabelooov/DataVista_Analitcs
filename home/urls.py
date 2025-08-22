
from django.contrib import admin
from django.urls import path, include
from .views import home, markets

urlpatterns = [
    path('', home, name='home'),
    path('markets/', markets, name='markets')
]