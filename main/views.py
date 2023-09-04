from django.shortcuts import render
from .models import Category
from .models import Brand
from .models import Product
from .models import Banner

#Home page
def home(request):
    banners=Banner.objects.all().order_by('-id')
    data=Product.objects.filter(is_featured=False).order_by('-id') #filter rest of is_featured- this can use show selected product only
    # print("Featured Products:", data)
    return render(request,'index.html',{'data':data,'banners':banners}) #Display data


#Category
def category_list(request):
    data=Category.objects.all().order_by('-id') #show all category in category page
    return render(request,'category_list.html',{'data':data})

#Brand
def brand_list(request):
    data=Brand.objects.all().order_by('-id')
    return render(request,'brand_list.html',{'data':data})

#Product list   viwe all products and filter
def product_list(request):
    data=Product.objects.all().order_by('-id')
    # return render(request,'product_list.html',{'data':data})
    return render(request,'product_list.html',
        {
            'data':data,
        }         
        )

#Product list according to Category
def category_product_list(request,cat_id):
    category=Category.objects.get(id=cat_id)
    data=Product.objects.filter(category=category).order_by('-id')
    return render(request,'category_product_list.html',{'data':data})

#Product list according to Brand
def brand_product_list(request,brand_id):
    brand=Brand.objects.get(id=brand_id)
    data=Product.objects.filter(brand=brand).order_by('-id')
    return render(request,'category_product_list.html',{'data':data})

#Product details
def product_detail(request,slug,id):
    slug=Product.objects.get(slug=slug)
    data=Product.objects.get(id=id)
    return render(request,'product_detail.html',{'data':data})
