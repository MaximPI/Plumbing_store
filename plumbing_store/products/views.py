from django.shortcuts import render

# Create your views here.

def index(request):
	return render(request, 'products/index.html')

def catalog(request):
	context = {
		"products": [
			{'name': 'PC', 'price': 500_000},
			{'name': 'NoteBook', 'price': 100_000},
			{'name': 'Phone', 'price': 30_000}
		]
	}
	return render(request, 'products/catalog.html', context=context)
