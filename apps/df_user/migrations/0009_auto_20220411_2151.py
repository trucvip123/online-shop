# Generated by Django 2.0.7 on 2022-04-11 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("df_user", "0008_auto_20220411_2130"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userinfo",
            old_name="usecurity_answer",
            new_name="uanswer",
        ),
        migrations.AddField(
            model_name="userinfo",
            name="usquestion",
            field=models.CharField(
                default="", max_length=40, verbose_name="security question"
            ),
        ),
    ]