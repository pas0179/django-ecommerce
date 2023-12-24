from django.db import models
from django.urls import reverse

# Import pillow pour redimensionner une image lors de l'import
from PIL import Image 




# Création de la table catégorie
class Category(models.Model):
	name = models.CharField(max_length=150)
	slug = models.SlugField(max_length=150, unique=True)
	image_cat = models.ImageField(upload_to="images", default=None, blank=True)

	class Meta:

		verbose_name = "categorie"
		verbose_name_plural = "categories"

	def __str__(self):
		return self.name
	


# Création de la table produit
class Product(models.Model):
	category = models.ForeignKey(
			Category,
			related_name="products",
			on_delete=models.CASCADE,
	)

	name = models.CharField(max_length=150)
	slug = models.SlugField(max_length=150)
	image = models.ImageField(upload_to='uploads/product/', blank=True)
	description = models.CharField(max_length=250, default='', blank=True, null=True)
	price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	quantity = models.IntegerField(default=0)


	def __str__(self):
		return self.name
	
	def view_stock(self):
		return self.quantity	

	def dropdown_list(self):
		"""
		Retourne un dictionnaire pour dropdown_list pour chaque produit
		"""
		quantity = self.view_stock()
		dropdown = {}
		for i in range(1, quantity + 1):
			dropdown[str(i)] = i
			i += 1
		return dropdown	
	

	max_width = 800

	# Fonction pour redimensionner automatiquement un image importé
	def resize_image(self):
		try:
			# Ouverture de l'image importé
			image = Image.open(self.image)

			# On récupère la taille d'origine de la photo importée
			width, height = image.size

			if width > self.max_width:
				coef = width // self.max_width

				new_width, new_height = width // coef, height // coef

				size = (new_width, new_height)

				# On resize l'image 
				image.thumbnail(size)

				# Sauvegarde de l'image resizer
				image.save(self.image.path)

		except:
			pass	

	
	# Sauvegarde automatique du redimensionement d'image lors d'import
	def save(self, *args, **kwargs):
		# On surcharge la méthode save de la classe pour image
		super().save(*args, **kwargs)
		if self.image != "":
			# lancement de la fonction resize_image
			self.resize_image()



class StockProduct(models.Model):
	name_product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity_in = models.IntegerField(default=0)
	quantity_out = models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.name_product)