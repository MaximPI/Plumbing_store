from django.db import models
from django.template.context_processors import request
from users.models import User
from decimal import Decimal, ROUND_HALF_UP
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
	power = models.PositiveIntegerField(blank=True)
	life = models.PositiveIntegerField()
	category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

	@property
	def rating(self):
		ratings = [review.rating for review in Review.objects.filter(product=self)]
		if ratings:
			rating = Decimal(str(sum(ratings) / len(ratings)))
		else:
			rating = Decimal("0")
		rating = rating.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
		return rating

	@property
	def quant_rating(self):
		ratings = [review for review in Review.objects.filter(product=self)]
		return len(ratings)

	def __str__(self):
		return f"{self.name} - {self.category.name}"

class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.product.name} - {self.user.username}"

	def summ(self):
		return self.quantity * self.product.price

class Baskets(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)
	created_timestamp = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"Корзина пользователя {self.user.username} | Продукт {self.product.name}"

	def summ(self):
		return self.quantity * self.product.price


class Favorites(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	created_timestamp = models.DateTimeField(auto_now_add=True)

	@property
	def rating(self):
		ratings = [review.rating for review in Review.objects.filter(product=self.product)]
		if ratings:
			rating = Decimal(str(sum(ratings) / len(ratings)))
		else:
			rating = Decimal("0")
		rating = rating.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
		return rating

	@property
	def quant_rating(self):
		ratings = [review for review in Review.objects.filter(product=self.product)]
		return len(ratings)

	def __str__(self):
		return f"Избранное пользователя {self.user.username} | Продукт {self.product.name}"


class Compare(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Review(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	rating = models.PositiveIntegerField(default=0)
	created_timestamp = models.DateTimeField(auto_now_add=True)
	description = models.TextField(blank=True)
	def __str__(self):
		return f"{self.user.username} | {self.product.name}"

