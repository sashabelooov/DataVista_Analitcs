from django.db import models

class Marketplace(models.Model):
    name = models.CharField(max_length=100)  # Masalan: Uzum, Ozon
    country = models.CharField(max_length=50)  # Davlat: Uzbekistan, Russia, Japan
    image = models.ImageField(upload_to="marketplaces/")  # Rasm yuklash
    created_at = models.DateField(auto_now_add=True)  # qachon yaratilgani

    def __str__(self):
        return self.name



class Shop(models.Model):
    name = models.CharField(max_length=50, unique=True)
    marketplace = models.ForeignKey("Marketplace", on_delete=models.CASCADE, related_name="shops")

    def __str__(self):
        return f"{self.name} ({self.marketplace.name})"



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    rating = models.FloatField(blank=True, null=True)
    comment_number = models.IntegerField(default=0)
    color = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        default="products/i.webp"  # default rasm
    )

    def __str__(self):
        return f"{self.title} ({self.shop.name})"
