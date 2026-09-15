from django.urls import path
from products.views import catalog, baskets, basket_add, basket_delete, basket_readd, favorites, favorite_add, favorite_delete

app_name = 'products'

urlpatterns = [
    path('', catalog, name='home'),
    path('baskets', baskets, name='baskets'),
    path('favorites', favorites, name='favorites'),
    path('basket-add/<int:product_id>', basket_add, name='basket_add'),
    path('basket-delete/<int:basket_id>', basket_delete, name='basket_delete'),
    path('basket-readd/<int:product_id>', basket_readd, name='basket_readd'),
    path('favorite-add/<int:product_id>', favorite_add, name='favorite_add'),
    path('favorite-delete/<int:favorite_id>', favorite_delete, name='favorite_delete'),
]