
from django import forms
from django.contrib import admin
from .models import Banner, Category,Brand,Color,Size,Product,ProductAttribute,CartOrder,CartOrderItems,UserAddressBook
from .models import TotalIncomeReport
from django.utils.html import format_html
from .models import CartOrder  # Import your CartOrder model


from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Sum
import datetime
from rangefilter.filter import DateRangeFilter






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
    list_display=('id','title','category','quantity','brand','color','size','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Product,ProductAdmin)

#ProductAttributeAdmin - This model is product has attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','product','image_tag','color','size','price')
admin.site.register(ProductAttribute,ProductAttributeAdmin)


# CartOrderAdmin
# class CartOrderAdmin(admin.ModelAdmin):
#     list_editable = ('paid_status','order_status')
#     list_display=('user','total_amt','order_dt','paid_status','order_status','payment_method','address')
# admin.site.register(CartOrder,CartOrderAdmin)


# class CartOrderItemsAdmin(admin.ModelAdmin):
#      list_display=('invoice_no','item','image_tag','qty','price','total')
# admin.site.register(CartOrderItems,CartOrderItemsAdmin)


class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'item', 'display_image', 'qty', 'price', 'total')

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
    display_image.short_description = 'Image'

admin.site.register(CartOrderItems, CartOrderItemsAdmin)

class UserAddressBookAdmin(admin.ModelAdmin):
	list_display=('user','address','mobile','mobile2','status')
admin.site.register(UserAddressBook,UserAddressBookAdmin)


@admin.register(TotalIncomeReport)
class TotalIncomeReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_income')
 

class DateRangeField(forms.fields.DateField):
    widget = admin.widgets.AdminDateWidget

class DateFilter(DateRangeFilter):
    def filter(self, request, queryset, value):
        if not value:
            return queryset
        date_field = self.field_name
        return queryset.filter(**{
            f'{date_field}__range': [
                datetime.datetime.combine(value.start, datetime.time.min),
                datetime.datetime.combine(value.stop, datetime.time.max),
            ]
        })

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ('paid_status', 'order_status')
    list_filter = (
        ('order_dt', DateFilter),  # Use the DateFilter for daily filtering
        'order_status',
        'paid_status',  # Add filter for paid_status
    )

    def total_income(self, obj):
        start_date = obj.order_dt
        end_date = obj.order_dt + datetime.timedelta(days=1)

        # Calculate daily income for paid orders
        income = CartOrder.objects.filter(
            order_dt__range=(start_date, end_date),
            paid_status=True
        ).aggregate(Sum('total_amt'))['total_amt__sum']

        return income

    total_income.short_description = "Total Income"  # Display name for the new field

    # Override the list_display property to add the new field
    list_display = ('user', 'total_amt', 'order_dt', 'paid_status', 'order_status', 'payment_method', 'address')

admin.site.register(CartOrder, CartOrderAdmin)
