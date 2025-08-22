from django.contrib import admin
from .models import Marketplace

@admin.register(Marketplace)
class MarketplaceAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "link", "created_at")
    search_fields = ("name", "country")