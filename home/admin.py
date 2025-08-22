from django.contrib import admin
from .models import Marketplace, Shop, Category, Product



@admin.register(Marketplace)
class MarketplaceAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "created_at")
    search_fields = ("name", "country")



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'shop', 'category', 'price', 'rating', 'comment_number', 'color')
    list_filter = ('shop', 'category', 'color')
    search_fields = ('title', 'shop__name', 'category__name')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)