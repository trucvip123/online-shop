# Generated by Django 2.0.7 on 2019-04-27 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("df_goods", "0002_auto_20181218_1200"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goodsinfo",
            name="gclick",
            field=models.IntegerField(default=0, verbose_name="点击量"),
        ),
        migrations.AlterField(
            model_name="goodsinfo",
            name="gkucun",
            field=models.IntegerField(default=0, verbose_name="库存"),
        ),
        migrations.AlterField(
            model_name="goodsinfo",
            name="gtitle",
            field=models.CharField(max_length=20, unique=True, verbose_name="商品名称"),
        ),
    ]