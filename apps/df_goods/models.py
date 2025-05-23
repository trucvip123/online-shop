from datetime import datetime

from django.db import models
from tinymce.models import HTMLField


# record the information of the category for each products
class TypeInfo(models.Model):
    # Product type
    id = models.BigAutoField(primary_key=True)
    isDelete = models.BooleanField(default=False)
    ttitle = models.CharField(max_length=20, verbose_name="categories")
    ntitle = models.CharField(max_length=50, verbose_name="category_name")

    class Meta:
        verbose_name = "product_category"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ttitle


class GoodsInfo(models.Model):
    isDelete = models.BooleanField(default=False)
    gtitle = models.CharField(max_length=100, verbose_name="goods_name", unique=True)
    gprice = models.DecimalField(
        max_digits=10, decimal_places=0, verbose_name="goods_price"
    )
    gprice_old = models.DecimalField(
        max_digits=10, decimal_places=0, verbose_name="goods_price_old", default=0
    )
    gunit = models.CharField(max_length=20, default="500g", verbose_name="unit_weight")
    gclick = models.IntegerField(verbose_name="click_count", default=0, null=False)
    gjianjie = models.CharField(max_length=200, verbose_name="short_inro")
    gkucun = models.IntegerField(verbose_name="stock", default=0)
    gcontent = HTMLField(max_length=200, verbose_name="descriptions")
    gparam = HTMLField(max_length=200, verbose_name="parameters")
    gtype = models.ForeignKey(
        TypeInfo, on_delete=models.CASCADE, verbose_name="category"
    )
    gbrand = models.CharField(max_length=50, verbose_name="brand", default="")
    gvideo_url = models.URLField(max_length=500, verbose_name="video_url", blank=True, null=True)

    class Meta:
        verbose_name = "products"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.gtitle


class ProductImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        GoodsInfo, related_name="images", on_delete=models.CASCADE
    )
    image_path = models.ImageField(
        verbose_name="goods_pic",
        upload_to="df_goods/images/%Y/%m",
        null=True,
        blank=True,
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Image Order")

    class Meta:
        ordering = ["order"]  # Ensures default sorting by order
