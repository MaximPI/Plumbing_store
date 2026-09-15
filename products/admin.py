from django.contrib import admin

# Register your models here.

from products.models import Product, ProductCategory, Order, Baskets, Favorites

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(Baskets)
admin.site.register(Favorites)

