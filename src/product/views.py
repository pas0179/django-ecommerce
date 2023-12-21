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

	# Création pour dropdown de la quantité en stock 
	# exemple: 5 produits en stock -> 1, 2, 3, 4, 5
	quantity = product.view_stock()

	# Lancement de la fonction dropdown
	stock = dropdown_quantity(quantity)	

	return render(request, 'product/product.html', {'product':product, "stock": stock})


def dropdown_quantity(quantity):
	stock = {}
	for i in range(1, quantity+1):
		stock[str(i)]= i
		i += 1

	return stock

