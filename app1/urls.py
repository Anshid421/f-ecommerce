from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.user_login,name='Login'),
    # path('products/', views.home, name='product_list'),
    path('shop/', views.shop, name='shop'),
    path('chair/', views.chair,name='chairs'),
    path('sofa/',views.sofa,name='sofa'),
    path('table/',views.table,name='table'),
    path('bed/',views.beds,name='beds'),
    path('out/',views.out,name='out'),
    path('about/',views.about,name='about'),
    path('service/',views.service,name='service'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('logot',views.logout_view,name='Logout'),
    path('profileform/',views.profile_form,name='Profileform'),
    
    
    
    path('cart/', views.cart_page, name='cart'),
    
    path('add-cart/<int:product_id>/', views.add_to_cart, name='add_cart'),
    
    path('checkout/<int:cart_id>/', views.checkout, name='checkout_one'),
    
    path('checkout/', views.checkout, name='checkout'),

    path('increase/<int:cart_id>/', views.increase_quantity, name='increase_qty'),

    path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_qty'),

    path('remove/<int:cart_id>/', views.remove_item, name='remove_item'),
    
    path('thankyou/', views.thankyou, name='thankyou'),
    
    path('my-orders/', views.my_orders, name='my_orders'),
    
    path('search/', views.search, name='search'),
    
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    
    
    path('wishlist/', views.wishlist_page, name='wishlist'),
    path('add-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_wishlist'),
    path('remove-wishlist/<int:id>/', views.remove_wishlist, name='remove_wishlist'),
]
