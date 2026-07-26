from django.contrib import admin

# Register your models here.

from products.models import Product, ProductCategory, User, Order

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(User)
admin.site.register(Order)

