# this file define the display and operation on the backstage management system
from django.contrib import admin

from .models import GoodsBrowser, UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["uname", "ufullname", "uyoubian", "uphone"]
    list_per_page = 5
    list_filter = ["uname", "uyoubian"]
    search_fields = ["uname", "uyoubian"]
    readonly_fields = ["uname"]


class GoodsBrowserAdmin(admin.ModelAdmin):
    list_display = ["user", "good"]
    list_per_page = 50
    list_filter = ["user__uname", "good__gtitle"]
    search_fields = ["user__uname", "good__gtitle"]
    readonly_fields = ["user", "good"]
    refresh_times = [3, 5]


admin.site.site_header = "Dien Thanh Liem Shop backstage management"
admin.site.site_title = "Dien Thanh Liem Shop backstage management"

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(GoodsBrowser, GoodsBrowserAdmin)
