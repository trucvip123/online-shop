# superuser: root 123123...
from django.contrib import admin

from .models import GoodsInfo, TypeInfo


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ["id", "ttitle", "ntitle"]
    list_per_page = 10
    search_fields = ["ttitle", "ntitle"]
    list_display_links = ["ttitle", "ntitle"]


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = [
        "id",
        "gtitle",
        "gtype",
        "gunit",
        "gclick",
        "gprice",
        "gkucun",
        "gbrand"
    ]
    list_editable = [
        "gkucun",
        "gtype"
    ]
    readonly_fields = ["gclick"]
    search_fields = ["gtitle"]
    list_display_links = ["gtitle"]


admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
