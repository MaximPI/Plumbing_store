from django.shortcuts import render, HttpResponseRedirect
from products.models import Product, ProductCategory, Baskets, Favorites
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
	context = {
		'title': 'Водная планета',
	}
	return render(request, 'products/index.html', context=context)

def catalog(request):
	context = {
		'title': 'каталог',
		'products': Product.objects.all(),
		'categories': ProductCategory.objects.all(),
		'baskets': [basket.product for basket in Baskets.objects.filter(user=request.user)],
		'bask': Baskets.objects.filter(user=request.user),
		'favorites': [favorite.product for favorite in Favorites.objects.filter(user=request.user)],
		'fav': Favorites.objects.filter(user=request.user),
		'quantity': len(Baskets.objects.filter(user=request.user)),
	}
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
def favorites(request):
	favoritess = Favorites.objects.filter(user=request.user)
	total_quantity = len(favoritess)
	context = {
		'title': 'Избранное',
		'favorites': Favorites.objects.filter(user=request.user),
		'total_quantity': total_quantity,
	}

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


