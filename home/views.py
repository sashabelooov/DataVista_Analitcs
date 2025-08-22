from django.shortcuts import render
from .models import Marketplace

def home(request):
    return render(request, 'home.html')


def markets(request):
    marketplaces = Marketplace.objects.all()
    return render(request, 'markets.html', {
        "marketplaces":marketplaces
    })