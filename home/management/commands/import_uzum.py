import csv
from django.core.management.base import BaseCommand
from ...models import Product, Shop, Category

class Command(BaseCommand):
    help = "Import Uzum products from CSV file"

    def handle(self, *args, **kwargs):
        file_path = "Data/cleaned_uzummarket.csv"

        # Uzum shop yaratamiz
        uzum_shop, _ = Shop.objects.get_or_create(name="Uzum")
        default_category, _ = Category.objects.get_or_create(name="Smartphones")

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                title = row["Title"]
                price = row["Price"]
                rating = row["Rating"]
                comment = row["Comment"]
                color = row["Color"]

                Product.objects.update_or_create(
                    title=title,
                    shop=uzum_shop,
                    defaults={
                        "category": default_category,
                        "price": price,
                        "rating": float(rating) if rating else None,
                        "comment_number": int(float(comment)) if comment else 0,
                        "color": color,
                    },
                )

        self.stdout.write(self.style.SUCCESS("✅ Uzum products imported successfully!"))
