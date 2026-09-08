from django.shortcuts import render, HttpResponseRedirect
from products.models import Product, ProductCategory, Baskets


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
		'categories': ProductCategory.objects.all()
	}
	return render(request, 'products/catalog.html', context=context)

def about(request):
	return render(request, 'products/about.html')

def baskets(request):
	context = {
		'title': 'Корзина',
		'baskets': Baskets.objects.filter(user=request.user),
	}
	return render(request, 'products/basket.html', context=context)

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

def basket_delete(request, basket_id):
	basket = Baskets.objects.get(id=basket_id)
	basket.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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