from django.db import models
from django.utils.html import mark_safe

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
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)
    
    class Meta:
      verbose_name_plural='6. Products'
    
    def __str__(self):
        return self.title

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
  
