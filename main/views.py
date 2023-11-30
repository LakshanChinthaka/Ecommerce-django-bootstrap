from django.shortcuts import redirect, render
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.db.models import Max,Min,Count
from .models import Category, Brand, Product,ProductAttribute,Banner
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.contrib.auth import login,authenticate
from .forms import SignupForm
#user try to checkout if user not login re derect to login page this| using below import code 
from django. contrib.auth.decorators import login_required 

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
    related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4] #[4] is show product count 
    colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct() #add multi colors for product details page
    sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__title','price','color__id').distinct()
    return render(request,'product_detail.html',{'data':product,'related': related_products,'colors':colors,'sizes':sizes})
    # return render(request, 'product_detail.html', {'data': product})

#Search
def search(request):
    q=request.GET['q']
    data=Product.objects.filter(title__icontains=q).order_by('-id') #q is quary
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
# def load_more_data (request):
#     offset=int(request.GET['offset'])
#     limit=int(request.GET['limit'])
#     data=Product.objects.all().order_by('-id')[offset:offset+limit]
#     data = render_to_string('ajax/product_list.html', {'data': data})
#     return JsonResponse({'data': data})

#add to cart
# def add_to_cart(request):
# 	# del request.session['cartdata']
# 	cart_p={}
# 	cart_p[str(request.GET['id'])]={
# 		'image':request.GET['image'], #image is not working
# 		'title':request.GET['title'],
# 		'qty':request.GET['qty'],
# 		'price':request.GET['price'],
# 	}
# 	if 'cartdata' in request.session:
# 		if str(request.GET['id']) in request.session['cartdata']:
# 			cart_data=request.session['cartdata']
# 			cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
# 			cart_data.update(cart_data)
# 			request.session['cartdata']=cart_data
# 		else:
# 			cart_data=request.session['cartdata']
# 			cart_data.update(cart_p)
# 			request.session['cartdata']=cart_data
# 	else:
# 		request.session['cartdata']=cart_p
  
        
# 	return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

    
# #cart list page
# def cart_list(request):
#     total_amt= 0
#     for p_id,item in request.session['cartdata'].items():
# 	    total_amt+=int(item['qty'])*float(item['price'])
     
#     return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

def cart_list(request):
    cart_data = request.session.get('cartdata', {})  # Use .get() to handle missing session data gracefully
    total_amt = 0

    for p_id, item in cart_data.items():
        qty = int(item.get('qty', 0))  # Use .get() to handle missing 'qty' gracefully
        price = float(item.get('price', 0))  # Use .get() to handle missing 'price' gracefully
        total_amt += qty * price

    return render(request, 'cart.html', {'cart_data': cart_data, 'totalitems': len(cart_data), 'total_amt': total_amt})


#cahtGpt add to chart
def add_to_cart(request):
    product_id = request.GET.get('id')
    image = request.GET.get('image')
    title = request.GET.get('title')
    qty = int(request.GET.get('qty'))
    price = float(request.GET.get('price'))

    cart_item = {
        'image': image,
        'title': title,
        'qty': qty,
        'price': price,
    }
    cart_data = request.session.get('cartdata', {})

    if product_id in cart_data:
        cart_data[product_id]['qty'] = qty
    else:
        cart_data[product_id] = cart_item
        
    request.session['cartdata'] = cart_data

    total_items = len(cart_data)
    return JsonResponse({'data': cart_data, 'totalitems': total_items})



#delete cart product
def delete_cart_item(request):
    p_id = str(request.GET.get('id'))  # Use get method to safely retrieve the ID
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del cart_data[p_id]  # Delete the item from the cart data
            request.session['cartdata'] = cart_data  # Update the session data

    total_amt = 0
    for item in request.session['cartdata'].values():
        total_amt += int(item['qty']) * float(item['price'])

    # Render the updated cart list using a template
    cart_list_html = render_to_string('ajax/cart-list.html', {
        'cart_data': request.session['cartdata'],
        'totalitems': len(request.session['cartdata']),
        'total_amt': total_amt,
    })
    return JsonResponse({'data': cart_list_html, 'totalitems': len(request.session['cartdata'])})

# Update Cart Item
def update_cart_item(request):
    p_id = str(request.GET.get('id'))
    p_qty = int(request.GET.get('qty'))  # Convert qty to integer
    
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[p_id]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty']) * float(item['price'])
    
    t = render_to_string('ajax/cart-list.html', {
        'cart_data': request.session['cartdata'],
        'totalitems': len(request.session['cartdata']),
        'total_amt': total_amt
    })
    
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})

#SignUp
def signup(request):
	if request.method=='POST':
		form=SignupForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			pwd=form.cleaned_data.get('password1')
			user=authenticate(username=username,password=pwd)
			login(request, user)
			return redirect('home')
	form=SignupForm
	return render(request, 'registration/signup.html',{'form':form})

#checkout page
#user try to checkout if user not login re derect to login page this| using below code 
@login_required
def checkout(request):
    total_amt =0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty']) * float(item['price']) 
        return render(request, 'checkout.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})