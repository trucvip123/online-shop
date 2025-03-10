# Generated by Django 5.1.6 on 2025-03-09 23:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("df_goods", "0004_remove_goodsinfo_gpic_goodsinfo_gprice_old"),
        ("df_user", "0004_userinfo_uaddress_detail_userinfo_ucommune_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userinfo",
            options={"verbose_name": "User", "verbose_name_plural": "Users"},
        ),
        migrations.RemoveField(
            model_name="userinfo",
            name="uaddress",
        ),
        migrations.RemoveField(
            model_name="userinfo",
            name="uaddress_detail",
        ),
        migrations.RemoveField(
            model_name="userinfo",
            name="ucommune",
        ),
        migrations.RemoveField(
            model_name="userinfo",
            name="udistrict",
        ),
        migrations.RemoveField(
            model_name="userinfo",
            name="uprovince",
        ),
        migrations.AlterField(
            model_name="goodsbrowser",
            name="good",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="browsed_by",
                to="df_goods.goodsinfo",
                verbose_name="Product",
            ),
        ),
        migrations.AlterField(
            model_name="goodsbrowser",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="browsing_history",
                to="df_user.userinfo",
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="uname",
            field=models.CharField(
                db_index=True, max_length=20, unique=True, verbose_name="Username"
            ),
        ),
        migrations.CreateModel(
            name="UserAddress",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "uprovince",
                    models.CharField(
                        default="", max_length=20, verbose_name="Province"
                    ),
                ),
                (
                    "udistrict",
                    models.CharField(
                        default="", max_length=20, verbose_name="District"
                    ),
                ),
                (
                    "ucommune",
                    models.CharField(default="", max_length=20, verbose_name="Commune"),
                ),
                (
                    "uaddress_detail",
                    models.CharField(
                        default="", max_length=100, verbose_name="Address Detail"
                    ),
                ),
                (
                    "default_address_flg",
                    models.BooleanField(default=False, verbose_name="Default Address"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="addresses",
                        to="df_user.userinfo",
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "User Address",
                "verbose_name_plural": "User Addresses",
            },
        ),
    ]
