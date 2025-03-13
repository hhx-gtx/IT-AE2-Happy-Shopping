from django.urls import path
from .views import (home, product_detail, cart_view, add_to_cart, update_cart,
                    order_detail_view, order_list_view, create_order_view,
                    direct_purchase_view, purchase_view, delete_orders_view, login_view, logout_view)




urlpatterns = [

    path('', login_view, name='login'),  # Default login page
    path('home/', home, name='home'),
    path('logout/', logout_view, name='logout'),  # Added exit/logout function

    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update_cart/<str:cart_key>/<str:action>/', update_cart, name='update_cart'),


    # path('order/detail/', order_detail_view, name='order_detail'),

    # path('order/latest/', latest_order_view, name='latest_order'),  # Show latest orders

    path('purchase/', purchase_view, name='purchase'),  # Shopping cart jump
    path('purchase/direct/', purchase_view, name='purchase_direct'),  # Jump to the buy now page
    path('buy-now/<int:product_id>/', direct_purchase_view, name='buy_now'),  # Buy Now Button


    path('order/create/', create_order_view, name='create_order'),  # Create an order after checkout
    path('order/<str:order_id>/', order_detail_view, name='order_detail'),  # Order details
    path('orders/', order_list_view, name='orders'),  # Order List
    path('orders/delete/', delete_orders_view, name='delete_orders'),


]

