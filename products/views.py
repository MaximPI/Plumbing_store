from django.contrib.admin.templatetags.admin_list import pagination
from django.shortcuts import render, HttpResponseRedirect
from products.models import Product, ProductCategory, Baskets, Favorites, Compare, Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.

def index(request):
	context = {
		'title': 'Водная планета',
	}
	return render(request, 'products/index.html', context=context)

def catalog(request, category_id=None, page_number=1):
	context = {
		'title': 'каталог',
		'categories': ProductCategory.objects.all(),
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
		filtered_products = Product.objects.filter(category_id=category_id)
	else:
		filtered_products = Product.objects.all()

	pagination = Paginator(filtered_products, 10)
	products_paginator = pagination.page(page_number)
	context.update({
		'products': products_paginator,
		'quantity': len(filtered_products),
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
	context = {
		'title': 'Страница товара',
		'product': Product.objects.get(id=product_id),
	}
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