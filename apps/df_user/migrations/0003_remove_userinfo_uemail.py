# Generated by Django 5.1.6 on 2025-03-05 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("df_user", "0002_alter_goodsbrowser_id_alter_userinfo_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userinfo",
            name="uemail",
        ),
    ]
