from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Category
from .stock import calcul_stock

# Create your views here.


def category(request, slug):
	"""
		si slug != "all" et slug dans Category alors on affiche la catégorie
		si slug == "all" alors tous les produits

	"""

	try:
		# Chercher la catégorie par rapport a la valeur de slug

		category = Category.objects.get(slug=slug)
		products = Product.objects.filter(category=category)
		

		return render(request, 'product/category.html', {
			'products':products,
			'category':category,
			})
	except:
		if slug == "all":
			products = Product.objects.all()
			category = "Tous les Produits"
			return render(request, 'product/category.html', {
				"products": products,
				"category": category,
				})
		else:
			messages.warning(request, ("Cette catégorie n'existe pas..."))
			return redirect('home')
	

def product(request,pk):
	calcul_stock()
	product = Product.objects.get(id=pk)
	return render(request, 'product/product.html', {'product':product})

