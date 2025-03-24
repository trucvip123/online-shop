from django.contrib import admin
from .models import OrderInfo, OrderDetailInfo

@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('oid', 'user', 'odate', 'oIsPay', 'ototal', 'oIsDelivery')
    search_fields = ('oid', 'user__uname')
    list_filter = ('oIsPay', 'oIsDelivery')
    ordering = ('-odate',)

@admin.register(OrderDetailInfo)
class OrderDetailInfoAdmin(admin.ModelAdmin):
    list_display = ('order', 'goods', 'price', 'count')
    search_fields = ('order__oid', 'goods__gtitle')
    list_filter = ('order__oIsPay',)
