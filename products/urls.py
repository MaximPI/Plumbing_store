from django.urls import path
from products.views import catalog

app_name = 'products'

urlpatterns = [
    path('', catalog, name='home'),
]