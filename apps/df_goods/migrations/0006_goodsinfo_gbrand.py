# Generated by Django 3.2.25 on 2025-03-14 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0005_goodsinfo_gparam'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsinfo',
            name='gbrand',
            field=models.CharField(default='', max_length=50, verbose_name='brand'),
        ),
    ]
