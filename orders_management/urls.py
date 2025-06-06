from django.urls import path
from . import views

urlpatterns = [
#     path('product/add/', views.AddProductView.as_view(), name='add_product_view'),
#     path('product/update/<int:id>/', views.UpdateProductView.as_view(), name='update_product_view'),
    path('products/', views.ListProductView.as_view(), name='list_products_view'),
    path('cart/add/', views.AddCartEntryView.as_view(), name='add_cart_entry'),
    path('cart/', views.ListCartEntriesView.as_view(), name='list_cart_entries'),
    path('payments/create/',views.InitiatePaymentView.as_view(), name='initiate_payments_view'),
    path('payments/callback/', views.RazorpayCallbackView.as_view(), name='razorpay-callback'),
    path('orders/', views.ListUserOrdersView.as_view(), name='list_user_orders'),
    path('orders/create/', views.CreateOrderView.as_view(), name='create_order_view'),
    # path('orders/delete/', views.DeleteOrderView.as_view(), name='delete_order_view'),
    # path('orders/update/'),
]

