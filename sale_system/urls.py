from django.contrib import admin
from django.urls import path, re_path

from profiles.views import (
    profile_view,
)
from accounts.views import (
    login_view,
    logout_view,
    register_view,
)
from products.views import (
    search_view,
    product_create_view,
    product_detail_view,
    product_update_view,
    product_list_view,
    product_api_detail_view,
)
from shopping_cart.views import (
    add_to_cart,
    delete_from_cart,
    order_details,
    checkout,
    process_payment,
    update_transaction_records,
    success,
)


urlpatterns = [    
    # home/root page
    path('', product_list_view,                                     name='home'),
    # accounts pages
    path('login/', login_view,                                      name='login'),
    path('logout/', logout_view,                                    name='logout'),
    path('register/', register_view,                                name='register'),
    # profile page
    path('profiles/', profile_view,                                 name='profile'),
    # product pages
    path('search/', search_view,                                    name='search'),
    path('products/', product_list_view,                            name='product_list'),
    path('products/create/', product_create_view,                   name='create_product'),
    path('products/<int:pk>/', product_detail_view,                 name='product_detail'),
    path('products/update/<int:pk>/', product_update_view,          name='update_product'),
    #shoping cart & checkout pages
    path('cart/add-to-cart/(?P<item_id>[-\w]+)/$', add_to_cart,     name='add_to_cart'),
    path('cart/order-summary/$', order_details,                     name='order_summary'),
    path('cart/success/$', success,                                 name='purchase_success'),
    path('cart/item/delete/(?P<item_id>[-\w]+)/$', delete_from_cart,name='delete_item'),
    path('cart/checkout/$', checkout,                               name='checkout'),
    path('cart/payment/(?P<order_id>[-\w]+)/$', process_payment,    name='process_payment'),
    path('cart/update-transaction/(?P<order_id>[-\w]+)/$', update_transaction_records, name='update_records'),

    re_path(r'api/products/(?P<pk>\d+)/', product_api_detail_view),
    
    path('admin/', admin.site.urls,                                 ), 

]
