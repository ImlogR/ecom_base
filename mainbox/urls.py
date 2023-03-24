from django.urls import path
from . import views

urlpatterns= [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('add_product/', views.add_product, name='add_product'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('processOrder/', views.processOrder, name='processOrder'),
    path('shop/', views.shop, name='shop'),
    path('view_product/<int:id>', views.view_product, name='view_product'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('update_product/<int:id>', views.update_product, name='update_product'),
]