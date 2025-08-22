# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Ensure this pattern is correct
    path('product_list/', views.product_list, name='product_list'),
    path('uzum_catalog/<int:marketplace_id>/', views.uzum_catalog, name='uzum_catalogs'),
    path("analytics/", views.marketplace_analytics, name="marketplace_analytics"),

]
