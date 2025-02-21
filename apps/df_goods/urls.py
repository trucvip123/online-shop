from django.urls import re_path as url

from . import views

app_name = "df_goods"

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^([a-zA-Z0-9-]+)_(\d+)_(\d+)/$", views.good_list, name="good_list"),
    url(r"^(\d+)/$", views.detail, name="detail"),
    url(r"^ordinary_search/", views.ordinary_search, name="ordinary_search"),
]
