from django.urls import path,include
# from django.contrib.auth import views as auth_views
from .import views

from django.conf import settings
from django.conf.urls.static import static
from .views import total_product_report_pdf
#user registration folder import from main. controller folder authview file 
# from main.controller import authview

urlpatterns = [
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('category_list',views.category_list,name='category_list'),
    path('brand_list',views.brand_list,name='brand_list'),
    path('product_list',views.product_list,name='product_list'),
    path('category_product_list/<int:cat_id>',views.category_product_list,name='category_product_list'),
    path('brand_product_list/<int:brand_id>',views.brand_product_list,name='brand_product_list'),
    path('product/<str:slug>/<int:id>/',views.product_detail, name='product_detail'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'), 
    path('cart',views.cart_list,name='cart'),
    path('delete-from-cart',views.delete_cart_item,name='delete_cart_item'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    path('accounts/signup/', views.signup, name='signup'),
    path('checkout',views.checkout,name='checkout'),
    #payment
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    #User section
    path('my-dashboard',views.my_dashboard, name='my_dashboard'),
    path('my-orders',views.my_orders, name='my_orders'),
    path('my-orders-items/<int:id>',views.my_order_items, name='my_order_items'),
    path('my-addressbook',views.my_addressbook, name='my-addressbook'),
    path('add-address',views.save_address, name='add-address'),
    path('activate-address',views.activate_address, name='activate-address'),
    path('edit-profile',views.edit_profile, name='edit-profile'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('cod', views.cash_on_delivery, name='cod'),
    path('order-sucess', views.order_success, name='order-sucess'),
    path('payment/', views.payment, name='payment'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #ADMIN SECTION
    path('orders-report/', views.test, name='orders-report'),
    path('daily-report/', views.daily_report, name='daily_report'),
    path('order_bar_chart/', views.order_bar_chart, name='order_bar_chart'),
    path('all-orders',views.all_orders, name='all_orders'),
    path('total_product_report_pdf/', total_product_report_pdf, name='total_product_report_pdf'),


]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




