#!/user/bin/env python
# -*- coding: utf-8 -*-
from django.urls import re_path as url

from . import views

app_name = "df_cart"

urlpatterns = [
    url(r"^$", views.user_cart, name="cart"),
    url(r"^add(\d+)_(\d+)/$", views.add, name="add"),
    url(r"^edit_(\d+)_(\d+)/$", views.edit, name="edit"),
    url(r"^delete(\d+)/$", views.delete, name="delete"),
]
