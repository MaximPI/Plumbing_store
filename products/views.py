from django.shortcuts import render, HttpResponseRedirect
from products.models import Product, ProductCategory, Baskets, Favorites, Compare, Order, Review
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from decimal import Decimal, ROUND_HALF_UP


# Create your views here.

def index(request):
	context = {
		'title': 'Водная планета',
	}
	products = {

	}

	if request.user.is_authenticated:
		context.update({
			'baskets': [basket.product for basket in Baskets.objects.filter(user=request.user)],
			'bask': Baskets.objects.filter(user=request.user),
		})
	for product in Product.objects.all():
		products[product] = len(Order.objects.filter(product=product))

	sorted_products = sorted(products.keys(), key=lambda x: products[x], reverse=True)
	context.update({
		'sorted_products': sorted_products[:4],
	})




	return render(request, 'products/index.html', context=context)

def catalog(request, category_id=None, page_number=1):
	context = {
		'title': 'каталог',
		'categories': ProductCategory.objects.all(),
		'if_categories': True,
		'ratings': [1, 2, 3, 4, 5],
	}

	if request.user.is_authenticated:
		context.update({
			'baskets': [basket.product for basket in Baskets.objects.filter(user=request.user)],
			'bask': Baskets.objects.filter(user=request.user),
			'favorites': [favorite.product for favorite in Favorites.objects.filter(user=request.user)],
			'fav': Favorites.objects.filter(user=request.user),
			'compares': Compare.objects.filter(user=request.user),
			'comp': [compare.product for compare in Compare.objects.filter(user=request.user)],
		})
	if category_id:
		products = Product.objects.filter(category_id=category_id)
	else:
		products = Product.objects.all()

	pagination = Paginator(products, 10)
	products_paginator = pagination.page(page_number)
	context.update({
		'products': products_paginator,
		'quantity': len(products),
		'category': category_id,
	})

	return render(request, 'products/catalog.html', context=context)


def about(request):
	return render(request, 'products/about.html')

@login_required
def baskets(request):
	basketss = Baskets.objects.filter(user=request.user)
	total_quantity = sum([basket.quantity for basket in basketss])
	total_sum = sum([basket.summ() for basket in basketss])
	context = {
		'title': 'Корзина',
		'baskets': Baskets.objects.filter(user=request.user),
		'total_quantity': total_quantity,
		'total_sum': total_sum,
	}

	return render(request, 'products/basket.html', context=context)

@login_required
def basket_add(request, product_id):
	product = Product.objects.get(id=product_id)
	baskets = Baskets.objects.filter(user=request.user, product=product)
	if not baskets.exists():
		Baskets.objects.create(user=request.user, product=product, quantity=1)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		basket = baskets.first()
		basket.quantity += 1
		basket.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_delete(request, basket_id):
	basket = Baskets.objects.get(id=basket_id)
	basket.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_readd(request, product_id):
	product = Product.objects.get(id=product_id)
	baskets = Baskets.objects.filter(user=request.user, product=product)
	if not baskets.exists():
		Baskets.objects.create(user=request.user, product=product, quantity=1)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		basket = baskets.first()
		if basket.quantity == 1:
			basket.delete()
		else:
			basket.quantity -= 1
			basket.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def favorites(request, page_number=1):
	favoritess = Favorites.objects.filter(user=request.user)
	total_quantity = len(favoritess)
	context = {
		'title': 'Избранное',
		'total_quantity': total_quantity,
		'baskets': [basket.product for basket in Baskets.objects.filter(user=request.user)],
		'bask': Baskets.objects.filter(user=request.user),
		'comp': [compare.product for compare in Compare.objects.filter(user=request.user)],
		'compares': Compare.objects.filter(user=request.user),
		'ratings': [1, 2, 3, 4, 5],
	}

	favorite = Favorites.objects.filter(user=request.user)
	pagination = Paginator(favorite, 10)
	products_paginator = pagination.page(page_number)
	context.update({
		'favorites': products_paginator,
	})
	return render(request, 'products/favorite.html', context=context)

@login_required
def favorite_add(request, product_id):
	product = Product.objects.get(id=product_id)
	Favorites.objects.create(user=request.user, product=product)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def favorite_delete(request, favorite_id):
	favorite = Favorites.objects.get(id=favorite_id)
	favorite.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def product_detail(request, product_id):
	product = Product.objects.get(id=product_id)
	reviews = [review.user for review in Review.objects.filter(product=product)]

	if request.user in reviews:
		user_reviewed = True
	else:
		user_reviewed = False

	context = {
		'title': 'Страница товара',
		'product': product,
		'user_reviewed': user_reviewed,
		'ratings': [1, 2, 3, 4, 5],
	}
	if request.user.is_authenticated:
		orders = [order.product for order in Order.objects.filter(user=request.user, product=product)]

		if orders:
			product_ordered = True
		else:
			product_ordered = False
		context.update({
			'product_ordered': product_ordered,
		})

	if request.user.is_authenticated:
		context.update({
			'baskets': [basket.product for basket in Baskets.objects.filter(user=request.user)],
			'bask': Baskets.objects.filter(user=request.user),
			'favorites': [favorite.product for favorite in Favorites.objects.filter(user=request.user)],
			'fav': Favorites.objects.filter(user=request.user),
			'comp': [compare.product for compare in Compare.objects.filter(user=request.user)],
			'compares': Compare.objects.filter(user=request.user),
		})

	return render(request, 'products/product_detail.html', context=context)

def compare(request):
	context = {
		'title': 'Сравнение товаров',
		'products': Compare.objects.filter(user=request.user),
		'bask': Baskets.objects.filter(user=request.user),
		'baskets': [basket.product for basket in Baskets.objects.filter(user=request.user)],
	}
	return render(request, 'products/compare.html', context=context)

def compare_readd(request, compare_id):
	compare = Compare.objects.get(id=compare_id)
	compare.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def compare_add(request, product_id):
	product = Product.objects.get(id=product_id)
	Compare.objects.create(user=request.user, product=product)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def orders(request):
	context = {
		'title': 'Заказы',
		'products': Order.objects.filter(user=request.user),
		'baskets': [basket.product for basket in Baskets.objects.filter(user=request.user)],
		'bask': Baskets.objects.filter(user=request.user),
		'favorites': [favorite.product for favorite in Favorites.objects.filter(user=request.user)],
		'fav': Favorites.objects.filter(user=request.user),
		'compares': Compare.objects.filter(user=request.user),
		'comp': [compare.product for compare in Compare.objects.filter(user=request.user)],
	}

	return render(request, 'products/orders.html', context=context)

def add_order(request):
	for basket in Baskets.objects.filter(user=request.user):
		Order.objects.create(user=request.user, product=basket.product, quantity=basket.quantity)
	basket = Baskets.objects.filter(user=request.user)
	basket.delete()
	return render(request, 'products/modal.html', context={})

def add_order_orders(request, order_id):
	order = Order.objects.get(id=order_id)
	Order.objects.create(user=request.user, product=order.product, quantity=order.quantity)
	return render(request, 'products/modal.html', context={})


def find(request):
	context = {
		'title': 'Каталог',
		'categories': ProductCategory.objects.all(),
		'if_categories': False
	}

	if request.user.is_authenticated:
		context.update({
			'baskets': [basket.product for basket in Baskets.objects.filter(user=request.user)],
			'bask': Baskets.objects.filter(user=request.user),
			'favorites': [favorite.product for favorite in Favorites.objects.filter(user=request.user)],
			'fav': Favorites.objects.filter(user=request.user),
			'compares': Compare.objects.filter(user=request.user),
			'comp': [compare.product for compare in Compare.objects.filter(user=request.user)],
		})

	name = request.GET.get('search', '').strip()
	products = Product.objects.filter(name__icontains=name)

	context.update({
		'products': products,
		'quantity': len(products),
	})
	return render(request, 'products/catalog.html', context=context)

def review(request, product_id):
	product = Product.objects.get(id=product_id)
	reviews = Review.objects.filter(product=product)
	context = {
		'reviews_count': len(Review.objects.filter(product=product)),
		'product': product,
		'ratings': [1, 2, 3, 4, 5],
	}
	review_users = [review.user for review in Review.objects.filter(product=product)]

	if request.user in review_users:
		user_reviewed = True
		user_review = Review.objects.get(product=product, user=request.user)
		reviews = [review for review in Review.objects.filter(product=product) if review.user != request.user]
		context.update({
			'user_review': user_review,
		})
	else:
		user_reviewed = False

	context.update( {
		'user_reviewed': user_reviewed,
		'reviews': reviews,
	})

	if request.user.is_authenticated:
		orders = [order.product for order in Order.objects.filter(user=request.user, product=product)]

		if orders:
			product_ordered = True
		else:
			product_ordered = False
		context.update({
			'product_ordered': product_ordered,
		})
	return render(request, 'products/review.html', context=context)

@login_required
def add_review(request, product_id):
	product = Product.objects.get(id=product_id)

	if request.method == 'POST':
		rating = request.POST.get('rating', '')
		description = request.POST.get('text', '')
		reviews = [review.user for review in Review.objects.filter(product=product)]
		if not request.user in reviews:
			Review.objects.create(user=request.user, product=product, rating=rating, description=description)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def rename_review(request, product_id):
	product = Product.objects.get(id=product_id)
	review = Review.objects.get(product=product, user=request.user)
	if request.method == 'POST':
		review.rating = request.POST.get('rating', '')
		review.description = request.POST.get('text', '')
		review.save()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def readd_review(request, product_id):
	product = Product.objects.get(id=product_id)
	review = Review.objects.get(product=product, user=request.user)
	review.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

