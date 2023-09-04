from django.contrib import admin
from .models import Banner
from .models import Category
from .models import Brand
from .models import Color
from .models import Size
from .models import Product
from .models import ProductAttribute

# admin.site.register(Banner)
admin.site.register(Brand)
admin.site.register(Size)

#BannerAdmin
class BannerAdmin(admin.ModelAdmin):
    list_display=('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

#CategoryAdmin
class CategoryAdmin(admin.ModelAdmin):
    list_display=('title','image_tag')
admin.site.register(Category,CategoryAdmin)

#ColorAdmin
class ColorAdmin(admin.ModelAdmin):
    list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

#ProductAdmin
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','category','brand','color','size','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Product,ProductAdmin)

#ProductAttributeAdmin - This model is product has attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','product','image_tag','color','size','price')
admin.site.register(ProductAttribute,ProductAttributeAdmin)

