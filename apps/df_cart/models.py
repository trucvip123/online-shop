from df_goods.models import GoodsInfo
from df_user.models import UserInfo
from django.db import models

# using foreign key to link the items in the cart to the user and the items


class CartInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="User")
    goods = models.ForeignKey(
        GoodsInfo, on_delete=models.CASCADE, verbose_name="products"
    )
    count = models.IntegerField(
        verbose_name="products_count", default=0
    )  # 记录用户买个多少单位的商品

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.uname + " cart"
