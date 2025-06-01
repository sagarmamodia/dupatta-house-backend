from django.urls import path
from . import views

urlpatterns = [
#     path('product/add/', views.AddProductView.as_view(), name='add_product_view'),
#     path('product/update/<int:id>/', views.UpdateProductView.as_view(), name='update_product_view'),
    path('products/', views.ListProductView.as_view(), name='list_products_view'),

    path('cart/add/', views.AddCartEntryView.as_view(), name='add_cart_entry'),
    path('cart/', views.ListCartEntriesView.as_view(), name='list_cart_entries'),
]

