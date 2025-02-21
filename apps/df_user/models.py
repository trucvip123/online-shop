from df_goods.models import GoodsInfo
from django.db import models
from django.utils import timezone


class UserInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    uname = models.CharField(max_length=20, unique=True, verbose_name="Username")
    upwd = models.CharField(max_length=40, verbose_name="Password", blank=False)
    uemail = models.EmailField(verbose_name="Email")
    ushou = models.CharField(max_length=20, default="", verbose_name="Shipping Address")
    uaddress = models.CharField(max_length=100, default="", verbose_name="Address")
    ufullname = models.CharField(max_length=30, default="", verbose_name="Full Name")
    uyoubian = models.CharField(max_length=6, default="", verbose_name="Zip Code")
    uphone = models.CharField(max_length=11, default="", verbose_name="Phone Number")
    uanswer = models.CharField(
        max_length=30, default="", verbose_name="Security Answer"
    )
    uquestion = models.CharField(
        max_length=40, default="", verbose_name="Security Question"
    )

    class Meta:
        verbose_name = "User_Info"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.uname


class GoodsBrowser(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="User")
    good = models.ForeignKey(
        GoodsInfo, on_delete=models.CASCADE, verbose_name="Product"
    )
    browser_time = models.DateTimeField(
        default=timezone.now, verbose_name="Browse Time"
    )

    class Meta:
        verbose_name = "Browsing History"
        verbose_name_plural = "Browsing Histories"

    def __str__(self):
        return f"{self.user.uname} viewed {self.good.gtitle}"
