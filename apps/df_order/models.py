from df_goods.models import GoodsInfo
from df_user.models import UserInfo
from django.db import models

# one model for record the whole order and the other record the information for each items in the order

class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True, verbose_name="order_no")
    user = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name="order_users", null=True, blank=True
    )
    odate = models.DateTimeField(auto_now=True, verbose_name="order_time")
    oIsPay = models.BooleanField(default=False, verbose_name="is_pay")
    ototal = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="total")
    oaddress = models.CharField(
        max_length=150, default="", verbose_name="order_address"
    )
    oreceiver = models.CharField(
        max_length=20, default="", verbose_name="order_receiver"
    )
    ocontact = models.CharField(
        max_length=11, default="", verbose_name="receiver_phone"
    )
    oIsDelivery = models.BooleanField(default=False, verbose_name="is_delivery")

    class Meta:
        verbose_name = "Orders"
        verbose_name_plural = verbose_name

    def __str__(self):
        user_name = self.user.uname if self.user else "Anonymous"
        return "{0} in order {1}".format(user_name, self.odate)


class OrderDetailInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    goods = models.ForeignKey(
        GoodsInfo, on_delete=models.CASCADE, verbose_name="products"
    )
    order = models.ForeignKey(
        OrderInfo, on_delete=models.CASCADE, verbose_name="orders"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=0, verbose_name="goods_price"
    )
    count = models.IntegerField(verbose_name="goods_count")

    class Meta:
        verbose_name = "order_details"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}(quantity{1})".format(self.goods.gtitle, self.count)
