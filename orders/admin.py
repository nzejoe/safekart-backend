from django.contrib import admin


from .models import OrderDetail, Payment, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['product', 'color', 'size',
                       'brand', 'quantity', 'price', 'total_amount', 'created']
    extra = 0

class OrderDetailAdmin(admin.ModelAdmin):
    model = OrderDetail
    list_display = ['order_number', 'user','total_amount', 'tax', 'grand_total', 'is_ordered','created']
    inlines = [OrderProductInline, ]

admin.site.register(Payment)
admin.site.register(OrderDetail, OrderDetailAdmin)
