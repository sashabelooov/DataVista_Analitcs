from django.shortcuts import render, get_object_or_404, redirect
from home.models import Marketplace, Product, Shop
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.db.models import Q
from home.models import Product, Marketplace
import base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from home.models import Marketplace, Product



def ozon_catalog(request, marketplace_id):
    marketplace = get_object_or_404(Marketplace, id=marketplace_id)

    if marketplace.id == 2:  # faqat Uzum (id=2)
        return render(request, 'ozon_catalog.html', {'marketplace': marketplace})
    
    else:
        marketplaces = Marketplace.objects.all()
        return render(request, 'markets.html', {
                "marketplaces":marketplaces
            })
    



def ozon_product_list(request):
    ozon_marketplace = get_object_or_404(Marketplace, id=2)
    products = Product.objects.filter(shop__name__icontains="Ozon").order_by("-rating")

    # products = Product.objects.filter(shop__marketplace=ozon_marketplace).order_by("-rating")

    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(color__icontains=query)
        )

    # Narx filtrlash
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    try:
        if min_price:
            min_price = float(min_price)
            if min_price < 0:
                raise ValidationError("Minimum price must be a positive number.")
            products = products.filter(price__gte=min_price)

        if max_price:
            max_price = float(max_price)
            if max_price < 0:
                raise ValidationError("Maximum price must be a positive number.")
            products = products.filter(price__lte=max_price)

    except (ValueError, ValidationError) as e:
        print(f"Invalid price input: {e}")
        products = products.none()

    return render(request, "item_ozon.html", {
        "products": products,
        "marketplace": ozon_marketplace
    })





def _fig_to_b64():
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()
    return "data:image/png;base64," + b64


def ozon_analytics(request):
    # Faqat Ozon (id=2) marketplaceni olish
    ozon_marketplace = get_object_or_404(Marketplace, id=2)
    qs = Product.objects.filter(shop__name__icontains="Ozon")

    if not qs.exists():
        return render(request, "ozon_analytics.html", {
            "img_minmax": None,
            "img_rating": None,
            "img_top_comments": None,
            "marketplace": ozon_marketplace
        })

    sns.set_theme(style="whitegrid")

    # 1) Eng arzon va qimmat
    min_product = qs.order_by("price").first()
    max_product = qs.order_by("-price").first()

    def safe_float(val):
        try:
            return float(str(val).replace(" ", "").replace(",", "").strip())
        except:
            return 0.0

    labels = [
        f"Arzon\n{min_product.title[:32]}",
        f"Qimmat\n{max_product.title[:32]}",
    ]
    values = [safe_float(min_product.price), safe_float(max_product.price)]

    plt.figure(figsize=(7, 4))
    ax = sns.barplot(x=labels, y=values, palette=["#2ecc71", "#e74c3c"])
    ax.set_title("Ozon: Eng arzon va eng qimmat mahsulotlar")
    ax.set_ylabel("Narx (so'm)")
    for p in ax.patches:
        v = p.get_height()
        ax.annotate(f"{v:,.0f}", (p.get_x() + p.get_width() / 2, v),
                    ha="center", va="bottom", fontsize=10, fontweight="bold")
    img_minmax = _fig_to_b64()

    # 2) Reyting taqsimoti
    def safe_rating(val):
        try:
            return float(str(val).replace(",", "."))
        except:
            return None

    ratings = [safe_rating(p.rating) for p in qs if p.rating]
    ratings = [r for r in ratings if r is not None]

    img_rating = None
    if ratings:
        plt.figure(figsize=(7, 4))
        ax = sns.histplot(ratings, bins=10, kde=True, color="#3498db")
        ax.set_title("Ozon: Reyting taqsimoti")
        ax.set_xlabel("Reyting")
        ax.set_ylabel("Mahsulotlar soni")
        img_rating = _fig_to_b64()

    # 3) Izohlar soni bo‘yicha TOP-10
    def safe_int(val):
        try:
            return int(str(val).replace(" ", "").replace("+", "").strip())
        except:
            return 0

    tops = sorted(
        [(p.title, safe_int(p.comment_number)) for p in qs],
        key=lambda x: x[1], reverse=True
    )[:10]

    img_top_comments = None
    if tops:
        titles = [t if len(t) <= 28 else t[:28] + "…" for t, _ in tops]
        counts = [c for _, c in tops]
        plt.figure(figsize=(8, 5))
        ax = sns.barplot(y=titles, x=counts, orient="h", palette="Set3")
        ax.set_title("Ozon: Izohlar soni bo‘yicha TOP-10")
        ax.set_xlabel("Izohlar soni")
        ax.set_ylabel("")
        for c, y in zip(counts, range(len(titles))):
            ax.text(c, y, f" {c}", va="center", ha="left", fontweight="bold")
        img_top_comments = _fig_to_b64()

    return render(request, "ozon_analytics.html", {
        "img_minmax": img_minmax,
        "img_rating": img_rating,
        "img_top_comments": img_top_comments,
        "min_product": min_product,
        "max_product": max_product,
        "marketplace": ozon_marketplace
    })

