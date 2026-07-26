from django.shortcuts import render
from products.models import Product, ProductCategory
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