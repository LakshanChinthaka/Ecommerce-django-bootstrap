from django.urls import path
from .import views

from django.conf import settings
from django.conf.urls.static import static

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
    path('load-more-data',views.load_more_data,name='load_more_data'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
