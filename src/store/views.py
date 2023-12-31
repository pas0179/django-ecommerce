from django.shortcuts import render
from product.models import Product
from product.task import calcul_stock_all_products

# Create your views here.

def home(request):
	# Lancement du calcul de stock pour tous les produits
	# lance avec celery en arriere plan
	products = Product.objects.all()[:4]
	for prod in products:
		print(prod.image)
	return render(request, 'store/home.html', {"products": products})
