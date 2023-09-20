from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.db.models import Max,Min,Count
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
    total_data=Product.objects.count()
    data=Product.objects.all().order_by('-id')[:3]  #[:10] is 10 products is display after load more display another products
    return render(request,'product_list.html',
        {
            'data':data,
            'total_data':total_data,
            # 'min_price':min_price,
            # 'max_price':max_price,
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
    product=Product.objects.get(id=id)
    related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
    return render(request,'product_detail.html',{'data':product,'related': related_products})
    # return render(request, 'product_detail.html', {'data': product})

#Search
def search(request):
    q=request.GET['q']
    data=Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request,'search.html',{'data':data})

#filter data
def filter_data(request):
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']

    # Start with all products
    allProducts = Product.objects.all().order_by('-id').distinct()

    # Apply price range filter
    allProducts = allProducts.filter(productattribute__price__gte=minPrice)
    allProducts = allProducts.filter(productattribute__price__lte=maxPrice)

    if colors:
        allProducts = allProducts.filter(productattribute__color__id__in=colors).distinct()

    if categories:
        allProducts = allProducts.filter(category__id__in=categories).distinct()

    if brands:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()

    if sizes:
        allProducts = allProducts.filter(productattribute__sizes__id__in=sizes).distinct()

    # Render the filtered products using a template
    data = render_to_string('ajax/product_list.html', {'data': allProducts})

    return JsonResponse({'data': data})

#load more
def load_more_data (request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    data=Product.objects.all().order_by('-id')[offset:offset+limit]
    data = render_to_string('ajax/product_list.html', {'data': data})
    return JsonResponse({'data': data})

