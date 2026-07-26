from django.db import models

# Create your models here.


class ProductCategory(models.Model):
	name = models.CharField(max_length=64, unique=True)
	description = models.TextField(blank=True)
	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=128, unique=True)
	image = models.ImageField(upload_to="products_media/", blank=True)
	description = models.TextField(blank=True)
	short_description = models.CharField(max_length=128, blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)
	length = models.PositiveIntegerField()
	width = models.PositiveIntegerField()
	height = models.PositiveIntegerField()
	power = models.PositiveIntegerField()
	life = models.PositiveIntegerField()
	category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
	def __str__(self):
		return f"{self.name} - {self.category.name}"

class User(models.Model):
	username = models.CharField(max_length=64, unique=True)
	password = models.CharField(max_length=128)
	phone = models.CharField(max_length=11)
	email = models.EmailField()
	def __str__(self):
		return self.username

class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.product.name} - {self.user.username}"






