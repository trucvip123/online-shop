# Generated by Django 3.2.25 on 2025-03-29 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0007_productimage_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='gvideo_url',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='video_url'),
        ),
    ]
