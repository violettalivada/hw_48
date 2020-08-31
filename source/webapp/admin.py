from django.contrib import admin
from .models import Product, Order,OrderProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'amount', 'price')
    list_display_links = ('pk', 'name')
    list_filter = ('category',)
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_name', 'user_phone', 'created_at']
    list_filter = ['created_at']


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'qty']


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
