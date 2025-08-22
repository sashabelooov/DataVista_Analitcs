from django.shortcuts import render, get_object_or_404
from home.models import Marketplace, Product, Shop
from django.db.models import Q
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import matplotlib



def uzum_catalog(request, marketplace_id):
    marketplace = get_object_or_404(Marketplace, id=marketplace_id)

    if marketplace.id == 1:  # faqat Uzum (id=1)
        return render(request, 'uzum_catalog.html', {'marketplace': marketplace})
    else:
        marketplaces = Marketplace.objects.all()
        return render(request, 'markets.html', {
                "marketplaces":marketplaces
            })
    


from django.core.exceptions import ValidationError

def product_list(request, marketplace_id=None):
    # Get the marketplace or use all marketplaces
    if marketplace_id:
        marketplace = get_object_or_404(Marketplace, id=marketplace_id)
        products = Product.objects.filter(shop__marketplace=marketplace).order_by("-rating")
    else:
        products = Product.objects.all().order_by("-rating")

    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(color__icontains=query)
        )

    # Price filters with validation
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    try:
        if min_price:
            min_price = float(min_price)
            if min_price < 0:
                raise ValidationError("Minimum price must be a positive number.")
            products = products.filter(price__gte=min_price)  # >= min_price

        if max_price:
            max_price = float(max_price)
            if max_price < 0:
                raise ValidationError("Maximum price must be a positive number.")
            products = products.filter(price__lte=max_price)  # <= max_price
    except (ValueError, ValidationError) as e:
        # Handle invalid price input
        print(f"Invalid price input: {e}")
        products = products.none()  # Show no products if invalid

    return render(request, "items.html", {"products": products, "marketplace": marketplace if marketplace_id else None})






matplotlib.use("Agg")
def _fig_to_b64():
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()
    return "data:image/png;base64," + b64

def marketplace_analytics(request):
    qs = Product.objects.all()
    print("Mahsulotlar soni:", qs.count())

    if not qs.exists():
        return render(request, "analytics.html", {
            "img_minmax": None, "img_rating": None, "img_top_comments": None
        })

    # Umumiy seaborn stili
    sns.set_theme(style="whitegrid")

    # -------- 1) Eng arzon va eng qimmat --------
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
    ax = sns.barplot(
        x=labels,
        y=values,
        palette=["#2ecc71", "#e74c3c"]  # yashil va qizil
    )
    ax.set_title("Eng arzon va eng qimmat telefonlar")
    ax.set_ylabel("Narx (so'm)")
    for p in ax.patches:
        v = p.get_height()
        ax.annotate(f"{v:,.0f}", (p.get_x() + p.get_width() / 2, v),
                    ha="center", va="bottom", fontsize=10, fontweight="bold")
    img_minmax = _fig_to_b64()

    # -------- 2) Reyting taqsimoti --------
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
        ax = sns.histplot(
            ratings, bins=10, kde=True, color="#3498db"  # ko‘k rang
        )
        ax.set_title("Reyting taqsimoti")
        ax.set_xlabel("Reyting")
        ax.set_ylabel("Mahsulotlar soni")
        img_rating = _fig_to_b64()

    # -------- 3) Izohlar soni bo‘yicha TOP-10 --------
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
        ax = sns.barplot(
            y=titles, x=counts, orient="h",
            palette="Set3"  # chiroyli turli rangli palitra
        )
        ax.set_title("Izohlar soni bo‘yicha TOP-10")
        ax.set_xlabel("Izohlar soni")
        ax.set_ylabel("")
        for c, y in zip(counts, range(len(titles))):
            ax.text(c, y, f" {c}", va="center", ha="left", fontweight="bold")
        img_top_comments = _fig_to_b64()

    return render(request, "analytics.html", {
        "img_minmax": img_minmax,
        "img_rating": img_rating,
        "img_top_comments": img_top_comments,
        "min_product": min_product,
        "max_product": max_product,
    })