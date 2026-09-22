from django.contrib import admin

# Register your models here.

from products.models import Product, ProductCategory, Order, Baskets, Favorites, Compare


admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(Baskets)
admin.site.register(Favorites)
admin.site.register(Compare)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'quantity')
	list_filter = ('category', 'price')
	search_fields = ('name',)
	ordering = ('name', 'category', 'price')
	fields = ('name', 'image', ('category', 'price', 'quantity'), ('length', 'width', 'height'), ('power', 'life'), 'description', 'short_description')

class BasketsAdmin(admin.TabularInline):
	model = Baskets
	readonly_fields = ('created_timestamp',)
	filter = ('name', 'quantity', 'created_timestamp',)