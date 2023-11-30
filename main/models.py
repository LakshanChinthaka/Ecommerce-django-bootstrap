from django.db import models
from django.utils.html import mark_safe
#import User for save to order to database 
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser

# from ecommerce.main.admin import CartOrderAdmin

#Banner
class Banner(models.Model):
    img=models.ImageField(upload_to="banner_imgs/")
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='1. Banners' #change order to admin dashboard
    
    def __str__(self):
        return self.alt_text
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="100"/>' % (self.img.url))

#Cetegory
class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cat_img/")
    
    class Meta:
        verbose_name_plural='2. Categorys'
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url)) #add category img to admin panal
    
    def __str__(self):
        return self.title

#Brand
class Brand(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="brand_img/")
    
    class Meta:
        verbose_name_plural='3. Brands'
    
    def __str__(self):
        return self.title  

#color
class Color(models.Model):
    title=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural='4. Colors'
    
    def color_bg(self):
          return mark_safe('<div style="width: 20px; height: 20px; background-color: %s"></div>' % (self.color_code)) #add color img to admin panal
    
    def __str__(self):
        return self.title

#Size
class Size(models.Model):
    title=models.CharField(max_length=100)
    
    class Meta:
      verbose_name_plural='5. Sizes'

    def __str__(self):
        return self.title
    
#Product
class Product(models.Model):
    title=models.CharField(max_length=100)
    slug=models.CharField(max_length=400)
    details=models.TextField()
    specs=models.TextField()
    quantity = models.PositiveIntegerField(default=0) 
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    # quantity = models.CharField(max_length=100)
  
    status=models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)
    
    class Meta:
      verbose_name_plural='6. Products'
    
    def __str__(self):
        return self.title
    
    
  #User address 
class UserAddressBook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=50,null=True)
    mobile2=models.CharField(max_length=50,null=True)
    address=models.TextField()
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='10. User Address'
    
    
    

#Product Attribute
class ProductAttribute(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    image=models.ImageField(upload_to="product_img/",null=True)
    
    class Meta:
      verbose_name_plural='7. ProductAttributes'
    
    def __str__(self):
        return self.product.title
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" height="70"/>' % (self.image.url))
  
 
  
# order
status_choice =(
    ('process', 'In Process'),
    ('deliverd', 'Deliverd') ,
    ('Dispatched','Dispatched'),
    ('Rejected','Rejected'),
    ('Returned','Returned')
)

payment_method = [
    ('online', 'Online'),
    ('cod', 'Cash on Delivery'),
]
class CartOrder(models.Model):
    #add  foreign key as User
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.ForeignKey(UserAddressBook,on_delete=models.CASCADE)
    total_amt = models.FloatField()
    paid_status = models.BooleanField(default=False)
    order_dt = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=status_choice,default='process',max_length=100)
    payment_method = models.CharField(choices=payment_method,default='none',max_length=100)
    address = models.CharField(max_length=100, null=True)
    
    class Meta:
      verbose_name_plural='8. Order'
    
    def image_tag(self):
     return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)

        
class CartOrderItems(models.Model):
    #ad CartOder as foreign key 
    order = models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    # image = models.CharField(max_length=200)
    image = models.ImageField(upload_to="cart_order_item_images/", null=True)  # Ensure it's an ImageField
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    
    class Meta:
      verbose_name_plural='9. Order Items'
      
      
      
class TotalIncomeReport(models.Model):
    date = models.DateField()
    total_income = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Income Report - {self.date}"
    
    


# class CustomStaff(AbstractUser):
#     mobile1 = models.CharField(max_length=50, blank=True, null=True)
#     mobile2 = models.CharField(max_length=50, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.username

