#!/user/bin/env python
# -*- coding: utf-8 -*-
# this is a command pattern and plays the role of route, the urls mapps the request from the template and send it to the specific function to operate.
from django.urls import re_path as url

from .views import *

app_name = "df_user"

urlpatterns = [
    url(r"^register/$", register, name="register"),
    url(r"^register_handle/$", register_handle, name="register_handle"),
    url(r"^register_exist/$", register_exist, name="register_exist"),
    url(r"^login/$", login, name="login"),
    url(r"^login_handle/$", login_handle, name="login_handle"),
    url(r"^info/$", info, name="info"),
    url(r"^order/(\d+)$", order, name="order"),
    url(r"^site/$", site, name="site"),
    url(r"^info_reset/$", info_reset, name="info_reset"),
    url(r"^insert_user_address/$", insert_user_address, name="insert_user_address"),
    url(r"^edit_user_address/$", edit_user_address, name="edit_user_address"),
    url(r"^site_handle/$", site_handle, name="site_handle"),
    # url(r'^place_order/$', views.place_order),
    url(r"^logout/$", logout, name="logout"),
    url(r"^forget_Password/$", forget_password, name="forget_password"),
    url(r"^forget_password/$", find_password, name="find_password"),
    url(r"^find_password/$", reset_handle, name="reset_handle"),
    url(r"^add_product/$", add_product, name="add_product"),
    url(r"^add_product_handle/$", add_product_handle, name="add_product_handle"),
    url(r"^edit_product/$", edit_product, name="edit_product"),
    url(r"^edit_product_handle/$", edit_product_handle, name="edit_product_handle"),
    url(
        r"^get_product_details_by_id/$",
        get_product_details_by_id,
        name="get_product_details_by_id",
    ),
    url(r"^add_new_type/$", add_new_type, name="add_new_type"),
    url(r"^edit_type/$", edit_type, name="edit_type"),
    url(r"^delete_type/$", delete_type, name="delete_type"),
    url(r"^manage_type/$", manage_type, name="manage_type"),
]
