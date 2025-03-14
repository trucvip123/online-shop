from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.static import serve

from apps import df_cart, df_goods, df_order, df_user

from .settings import MEDIA_ROOT

# this is a route role, the request in the templates like the form will link to a url, and the route will assign the request to specific function to process the request.
# it's a command pattern, the templates on the front end like a invoker, and the route in this file plays the role of command and delegate the request to the specific function
# receiver to execute, the template doesn't know the request will sent to whom.
urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^", include("df_goods.urls", namespace="df_goods")),
    url(r"^user/", include("df_user.urls", namespace="df_user")),
    url(r"^cart/", include("df_cart.urls", namespace="df_cart")),
    url(r"^order/", include("df_order.urls", namespace="df_order")),
    url(r"^tinymce/", include("tinymce.urls")),  # it's a tool for HTML rich text editor
    url(r"^media/(?P<path>.*)$", serve, {"document_root": MEDIA_ROOT}),
]
