from df_goods.models import GoodsInfo
from django.db import models
from django.utils import timezone


class UserInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    uname = models.CharField(
        max_length=20, unique=True, verbose_name="Username", db_index=True
    )
    upwd = models.CharField(max_length=40, verbose_name="Password", blank=False)
    ushou = models.CharField(max_length=20, default="", verbose_name="Shipping Address")
    ufullname = models.CharField(max_length=30, default="", verbose_name="Full Name")
    uyoubian = models.CharField(max_length=6, default="", verbose_name="Zip Code")
    uphone = models.CharField(max_length=11, default="", verbose_name="Phone Number")
    uanswer = models.CharField(
        max_length=30, default="", verbose_name="Security Answer"
    )
    uquestion = models.CharField(
        max_length=40, default="", verbose_name="Security Question"
    )
    is_staff = models.BooleanField(default=False, verbose_name="Is Admin")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.uname


class GoodsBrowser(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
        related_name="browsing_history",
        verbose_name="User",
    )
    good = models.ForeignKey(
        GoodsInfo,
        on_delete=models.CASCADE,
        related_name="browsed_by",
        verbose_name="Product",
    )
    browser_time = models.DateTimeField(
        default=timezone.now, verbose_name="Browse Time"
    )

    class Meta:
        verbose_name = "Browsing History"
        verbose_name_plural = "Browsing Histories"

    def __str__(self):
        return f"{self.user.uname} viewed {self.good.gtitle} on {self.browser_time.strftime('%Y-%m-%d %H:%M:%S')}"


class UserAddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        UserInfo,
        related_name="addresses",
        on_delete=models.CASCADE,
        verbose_name="User",
    )
    uprovince = models.CharField(max_length=20, default="", verbose_name="Province")
    udistrict = models.CharField(max_length=20, default="", verbose_name="District")
    ucommune = models.CharField(max_length=20, default="", verbose_name="Commune")
    uaddress_detail = models.CharField(
        max_length=100, default="", verbose_name="Address Detail"
    )
    default_address_flg = models.BooleanField(
        default=False, verbose_name="Default Address"
    )

    class Meta:
        verbose_name = "User Address"
        verbose_name_plural = "User Addresses"

    def __str__(self):
        return f"{self.user.uname} - {self.uaddress_detail} ({'Default' if self.default_address_flg else 'Secondary'})"
