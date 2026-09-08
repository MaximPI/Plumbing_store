from django.urls import path
from products.views import catalog, baskets, basket_add, basket_delete, basket_readd

app_name = 'products'

urlpatterns = [
    path('', catalog, name='home'),
    path('baskets', baskets, name='baskets'),
    path('basket-add/<int:product_id>', basket_add, name='basket_add'),
    path('basket_delete/<int:basket_id>', basket_delete, name='basket_delete'),
    path('basket_readd/<int:product_id>', basket_readd, name='basket_readd'),
]