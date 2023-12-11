
import datetime
from django.shortcuts import redirect, render
from django.conf import settings
from django.shortcuts import render, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.db.models import Max,Min,Count
from .models import Category, Brand, Product,ProductAttribute,Banner,CartOrder,CartOrderItems,UserAddressBook
from main.models import CartOrder
from django.template.loader import render_to_string
from django.contrib.auth import login,authenticate
from .forms import SignupForm,AddressBookForm,ProfileForm
from django.contrib.auth.decorators import login_required 
import calendar


from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as auth_logout 
from django.utils import timezone 

#paypal
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.db.models import Sum

#for chart
from django.db.models.functions import ExtractMonth
from xhtml2pdf import pisa
from django.template.loader import get_template
import datetime
from reportlab.pdfgen import canvas
from datetime import datetime
from django.db.models.functions import ExtractDay
from django.utils.html import mark_safe






#Home page
def home(request):
    banners=Banner.objects.all().order_by('-id')
    data=Product.objects.filter(is_featured=False).order_by('-id') #filter rest of is_featured- this can use show selected product only
    # print("Featured Products:", data)
    # print('Home Product - ',data )
    product_ids = [product.id for product in data]
    print('Product IDs:', product_ids)
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
    # category=Category.objects.get(id=cat_id)
    category = get_object_or_404(Category, id=cat_id)
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
    print("Product Id Cart - " , product_id)

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
    # price("Product ID -" , product_id)

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



@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')


# Dashboard
import calendar
@login_required
def my_dashboard(request):
    # orders=CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month','count')
    orders = CartOrder.objects.filter(user=request.user).annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month', 'count')
    monthNumber=[]
    totalOrders=[]
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    return render(request, 'user/dashboard.html',{'monthNumber':monthNumber,'totalOrders':totalOrders})
##################################
# My Orders
@login_required
def my_orders(request):
    # Get all orders for the particular user
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    # return render(request, 'user/orders.html', {'orders': orders})
    return render(request, 'user/orders.html',{'orders':orders})

# Order Detail
@login_required
def my_order_items(request, id):
    order = get_object_or_404(CartOrder, pk=id)
    orderitems = CartOrderItems.objects.filter(order=order).order_by('-id')
    return render(request, 'user/order-items.html', {'orderitems': orderitems})

@login_required
def my_addressbook(request):
	addbook=UserAddressBook.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/addressbook.html',{'addbook':addbook})

# Save addressbook
@login_required
def save_address(request):
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm
	return render(request, 'user/add-address.html',{'form':form,'msg':msg})

# Activate address
@login_required
def activate_address(request):
	a_id=str(request.GET['id'])
	UserAddressBook.objects.update(status=False)
	UserAddressBook.objects.filter(id=a_id).update(status=True)
	return JsonResponse({'bool':True})


# Edit Profile
def edit_profile(request):
	msg=None
	if request.method=='POST':
		form=ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=ProfileForm(instance=request.user)
	return render(request, 'user/edit-profile.html',{'form':form,'msg':msg})


# Update addressbook
def update_address(request,id):
	address=UserAddressBook.objects.get(pk=id)
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST,instance=address)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm(instance=address)
	return render(request, 'user/update-address.html',{'form':form,'msg':msg})

# Admin Profile
# Edit Profile
def admin_profile(request):
	msg=None
	if request.method=='POST':
		form=ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=ProfileForm(instance=request.user)
	return render(request, 'adminDashboard/edit-profile.html',{'form':form,'msg':msg})


# Update addressbook
def admin_update_address(request,id):
	address=UserAddressBook.objects.get(pk=id)
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST,instance=address)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm(instance=address)
	return render(request, 'adminDashboard/update-address.html',{'form':form,'msg':msg})




from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm

def signup(request):
    form  = SignupForm()
   
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            form.save()
            return redirect('payment')  # Replace 'home' with your desired redirect URL
  
    
    return render(request, 'registration/signup.html', {'form': form})


def payment(request):
    
    return render(request, 'payment.html')





from django.contrib.auth.decorators import login_required, user_passes_test

@user_passes_test(lambda u: u.is_staff, login_url='admin:login')
def dashboard(request):
    return render(request, 'yourapp/dashboard.html')



from django.db.models import Sum

def OrderReport(request):
    
     # Get all orders for the particular user
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    
    # Calculate the total income by summing the 'total_amt' field from CartOrder
    total_income = CartOrder.objects.filter(user=request.user).filter(paid_status=True).aggregate(total_income=Sum('total_amt'))
    
    # Retrieve the total income value from the result
    total_income = total_income['total_income'] if total_income['total_income'] else 0.0
    
    return render(request, 'adminDashboard/orders-report.html', {'orders': orders, 'total_income': total_income})


# Daily report
def daily_report(request):
    current_date = timezone.now()

    try:
        selected_day = int(request.GET.get('day', current_date.day))
        selected_month = int(request.GET.get('month', current_date.month))
        selected_year = int(request.GET.get('year', current_date.year))

        # Check if the selected date is within a valid range
        if selected_day < 1 or selected_day > 31 or selected_month < 1 or selected_month > 12 or selected_year < 2000:
            raise ValueError("Invalid date, month, or year")

        start_date = timezone.datetime(selected_year, selected_month, selected_day)
        end_date = start_date + timezone.timedelta(days=1)  # Add one day to get the next day

        paid_orders = CartOrder.objects.filter(
            paid_status=True,
            order_dt__range=(start_date, end_date)
        )

        total_income = paid_orders.aggregate(Sum('total_amt'))['total_amt__sum'] or 0

        context = {
            'paid_orders': paid_orders,
            'total_income': total_income,
            'selected_day': selected_day,
            'selected_month': selected_month,
            'selected_year': selected_year,
        }

        return render(request, 'adminDashboard/orders-report.html', context)
    except ValueError:
        return HttpResponse("Invalid date, month, or year selected.")




def test(request):

    # Filter paid orders for the currently authenticated user
    orders = CartOrder.objects.filter(user=request.user, paid_status=True).order_by('-id')
    
    # Calculate the total paid income by summing the 'total_amt' field from paid orders
    total_income = orders.aggregate(total_income=Sum('total_amt'))['total_income'] or 0.0
   
    return render(request, 'adminDashboard/orders-report.html',{'orders':orders, 'total_income':total_income})


# Cash On Delivery
def cash_on_delivery(request):
    total_amt = 0
    totalAmt = 0
    user = request.user
    user_address = UserAddressBook.objects.filter(user=user, status=True).first()

    # Check if 'cartdata' exists in the session
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            totalAmt += int(item['qty']) * float(item['price'])
        
        if user_address:
            # Create a new order and associate it with the user's address
            order = CartOrder(
                user=user,
                address=user_address.address,
                total_amt=totalAmt,
            )
            order.save()
            
            # Create order items
            for p_id, item in request.session['cartdata'].items():
                total_amt += int(item['qty']) * float(item['price'])
                
                item = CartOrderItems.objects.create(
                    order=order,
                    invoice_no='INV-' + str(order.id),
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=int(item['qty']) * float(item['price'])
                )

            # Update the paid_status to True after payment is made
            order.paid_status = False
            order.payment_method = 'cod'
            order.save()

            # Clear the cart after placing the order
            # del request.session['cartdata']

            # Decrease the product quantity after the order
            for p_id, item in request.session['cartdata'].items():
                try:
                    product_Id = Product.objects.get(id=p_id)
                    if product_Id.quantity >= int(item['qty']):
                        product_Id.quantity -= int(item['qty'])
                        product_Id.save()
                    else:
                        return HttpResponseBadRequest("Insufficient quantity for some products in the order")
                except ProductAttribute.DoesNotExist:
                    return HttpResponseBadRequest("ProductAttribute with ID {} does not exist".format(p_id))

    address = UserAddressBook.objects.filter(user=request.user, status=True).first()

    return render(request, 'cod.html', {
        'cart_data': request.session.get('cartdata', {}),
        'totalitems': len(request.session.get('cartdata', {})),
        'total_amt': total_amt,
        'address': address,
    })
    
# Order success
def order_success(request):

    latest_order = CartOrder.objects.filter(user=request.user).order_by('-id').first()
    del request.session['cartdata']
    return render(request, 'order-sucess.html', {'latest_order': latest_order})



@csrf_exempt
def payment_done(request):
    returnData = request.POST
    order_id = request.session.get('current_order_id')

    if order_id:
        # Fetch the order using the retrieved ID
        order = CartOrder.objects.get(id=order_id)

        # After payment is successful, decrease the product quantity
        order_items = CartOrderItems.objects.filter(order=order)
        for item in order_items:
            product = Product.objects.get(title=item.item)
            if product.quantity >= item.qty:
                product.quantity -= item.qty
                product.save()

    latest_order = CartOrder.objects.filter(user=request.user).order_by('-id').first()

    del request.session['cartdata']
    return render(request, 'payment-success.html', {'data': returnData, 'latest_order': latest_order})

@login_required
def checkout(request):
    total_amt = 0
    totalAmt = 0
    user = request.user
    user_address = UserAddressBook.objects.filter(user=user, status=True).first()

    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            totalAmt += int(item['qty']) * float(item['price'])

        if user_address:
            # Create a new order and associate it with the user's address
            order = CartOrder(
                user=user,
                address=user_address.address,
                total_amt=totalAmt,
            )
            order.save()

            # Create order items
            for p_id, item in request.session['cartdata'].items():
                total_amt += int(item['qty']) * float(item['price'])
                
                item = CartOrderItems.objects.create(
                    order=order,
                    invoice_no='INV-'+str(order.id),
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=int(item['qty']) * float(item['price'])
                )

    # Process payment
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total_amt,
        'item_name': 'OrderNo-'+ str(order.id),
        'invoice': 'INV-'+ str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
    }
   
    form = PayPalPaymentsForm(initial=paypal_dict)
    form.render()

    # Decrease the product quantity after the order
    for p_id, item in request.session['cartdata'].items():
        try:
            product_Id = Product.objects.get(id=p_id)
            if product_Id.quantity >= int(item['qty']):
                product_Id.quantity -= int(item['qty'])
                product_Id.save()
            else:
                return HttpResponseBadRequest("Insufficient quantity for some products in the order")
        except ProductAttribute.DoesNotExist:
            return HttpResponseBadRequest("ProductAttribute with ID {} does not exist".format(p_id))

    # Update the paid_status to True after payment is made
    order.paid_status = True
    order.payment_method = 'online'
    order.save()

    address = UserAddressBook.objects.filter(user=request.user, status=True).first()

    return render(request, 'checkout.html', {
        'cart_data': request.session['cartdata'],
        'totalitems': len(request.session['cartdata']),
        'total_amt': total_amt,
        'form': form,
        'address': address,
        'order': order,
    })



from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import ExtractDay
from django.contrib.auth.decorators import login_required
from .models import CartOrder
from django.utils import timezone  # Import the timezone module

@login_required
def daily_report(request):
    selected_date = request.GET.get('date')

    # Filter orders by the selected date or use the current date if not selected
    orders = CartOrder.objects.filter(
        user=request.user,
        order_dt__date=selected_date if selected_date else timezone.now().date()
    )

    total_orders = orders.count()
    total_income = orders.aggregate(Sum('total_amt'))['total_amt__sum']

    context = {
        'selected_date': selected_date,
        'total_orders': total_orders,
        'total_income': total_income,
        'orders': orders,
    }

    return render(request, 'adminDashboard/daily-report.html', context)


@login_required
def all_orders(request):
    # Get all orders for the particular user
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'adminDashboard/all-orders.html',{'orders':orders})


def total_product_report_pdf(request):
   
    orders = CartOrder.objects.all().order_by('-order_dt')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=total_orders_report.pdf'

    p = canvas.Canvas(response)

   
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, 'Orders Report')


    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, f'Report generated on: {current_date}')

    # Set up the header row
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 750, 'Order ID')
    p.drawString(200, 750, 'User')
    p.drawString(300, 750, 'Total Amount')
    p.drawString(400, 750, 'Payment Status')
    p.drawString(500, 750, 'Order Status')
    # p.drawString(400, 750, 'Order Time')

    # Set up the content for each order
    p.setFont("Helvetica", 10)
    y_position = 730  # Starting y position

    for order in orders:
        p.drawString(100, y_position, str(order.id))
        p.drawString(200, y_position, str(order.user))
        p.drawString(300, y_position, str(order.total_amt))
        p.drawString(400, y_position, 'Paid' if order.paid_status else 'Not yet Paid')
        p.drawString(500, y_position, order.order_status)
        # p.drawString(400, y_position, str(order.order_dt))

     
        y_position -= 20

    
    p.showPage()
    p.save()

  
    return response

# Bar chart
@login_required
def order_bar_chart(request):
    print("barchart")
    orders = CartOrder.objects.filter(user=request.user).annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month', 'count')

    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])

    return render(request, 'adminDashboard/order_bar_chart.html', {'monthNumber': monthNumber, 'totalOrders': totalOrders})




