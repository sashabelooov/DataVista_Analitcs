from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('ozon_catalog/<int:marketplace_id>/', views.ozon_catalog, name="ozon_catalog"),
    path('ozon_product_list/', views.ozon_product_list, name='ozon_product_list'),
    path('ozon_analytics/', views.ozon_analytics, name='ozon_analytics'),

]