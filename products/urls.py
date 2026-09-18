from django.urls import path
from products.views import catalog, baskets, basket_add, basket_delete, basket_readd, favorites, favorite_add, favorite_delete, product_detail


app_name = 'products'

urlpatterns = [
    path('', catalog, name='home'),
    path('baskets', baskets, name='baskets'),
    path('favorites', favorites, name='favorites'),
    path('product_detail/<int:product_id>', product_detail, name='product_detail'),
    path('basket-add/<int:product_id>', basket_add, name='basket_add'),
    path('basket-delete/<int:basket_id>', basket_delete, name='basket_delete'),
    path('basket-readd/<int:product_id>', basket_readd, name='basket_readd'),
    path('favorite-add/<int:product_id>', favorite_add, name='favorite_add'),
    path('favorite-delete/<int:favorite_id>', favorite_delete, name='favorite_delete'),
    path('<int:category_id>', catalog, name='category'),
    path('page/<int:page_number>', catalog, name='page_number'),
    path('favorite_page/<int:page_number>', favorites, name='favorite_page_number'),
    path('category/<int:category_id>/page/<int:page_number>', catalog, name='category_page'),
]