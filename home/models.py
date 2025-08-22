from django.db import models


class Marketplace(models.Model):
    name = models.CharField(max_length=100)  # Masalan: Uzum, Ozon
    country = models.CharField(max_length=50)  # Davlat: Uzbekistan, Russia, Japan
    link = models.URLField()  # Marketplace URL
    image = models.ImageField(upload_to="marketplaces/")  # Rasm yuklash
    created_at = models.DateField(auto_now_add=True)  # qachon yaratilgani

    def __str__(self):
        return self.name
