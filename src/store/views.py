from django.shortcuts import render
from product.models import Product
from product.stock import calcul_stock

# Create your views here.

def home(request):
	calcul_stock()
	products = Product.objects.all()[:4]
	for prod in products:
		print(prod.image)
	return render(request, 'store/home.html', {"products": products})
