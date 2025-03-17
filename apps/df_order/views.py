from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal

from df_cart.models import CartInfo
from df_user import user_decorator
from df_user.models import UserInfo
from df_goods.models import GoodsInfo
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render
from django.db.models import Sum

from .models import OrderDetailInfo, OrderInfo


class Strategy(ABC):
    @abstractmethod
    def calculate(self):
        pass


class freestrategy(Strategy):
    def calculate(self):
        return 0


class normalstrategy(Strategy):
    def calculate(self):

        return 10


class Shippingfee:
    strategy: Strategy

    def __init__(self, price, strategy):
        self.price = price
        self.strategy = strategy

    def calculate(self):
        shipcost = self.strategy.calculate()
        return shipcost


def order(request):
    user_id = request.session.get("user_id")  # Có thể là None nếu chưa đăng nhập
    cart_items = []
    total_price = 0

    if user_id:
        receiver = UserInfo.objects.get(id=user_id)
        cart_queryset = CartInfo.objects.filter(user_id=user_id)
        for cart in cart_queryset:
            cart_items.append(cart)
            total_price += float(cart.count) * float(cart.goods.gprice)
        total_count = cart_queryset.aggregate(Sum("count"))["count__sum"] or 0

    else:
        receiver = None  # Khách chưa có thông tin người nhận
        guest_cart = request.session.get("guest_cart", {})
        for goods_id, count in guest_cart.items():
            goods = GoodsInfo.objects.get(pk=goods_id)
            cart_items.append({"goods": goods, "count": count})
            total_price += float(count) * float(goods.gprice)
        total_count = sum(guest_cart.values())

    total_price = round(total_price, 2)

    # Tính phí vận chuyển
    if total_price > 50:
        shipping = Shippingfee(total_price, freestrategy())
    else:
        shipping = Shippingfee(total_price, normalstrategy())

    trans_cost = shipping.calculate()
    total_trans_price = trans_cost + total_price

    context = {
        "title": "submit order",
        "page_name": 1,
        "user": receiver,
        "carts": cart_items,
        "total_price": total_price,
        "trans_cost": trans_cost,
        "total_trans_price": total_trans_price,
        "cart_num": total_count,
    }

    return render(request, "df_order/place_order.html", context)


# @user_decorator.login
@transaction.atomic()
@transaction.atomic()
def order_handle(request):
    tran_id = transaction.savepoint()
    user_id = request.session.get("user_id")  # Có thể None nếu là khách
    address = request.POST.get("address")
    receiver = request.POST.get("receiver")
    phone = request.POST.get("contact")
    data = {}

    try:
        order_info = OrderInfo()
        now = datetime.now()
        order_info.oid = "%s%d" % (now.strftime("%Y%m%d%H%M%S"), user_id or 0)  # Nếu là khách thì dùng 0
        order_info.odate = now
        order_info.ototal = Decimal(request.POST.get("total"))
        order_info.oaddress = address
        order_info.ocontact = phone
        order_info.oreceiver = receiver

        if user_id:
            order_info.user_id = int(user_id)  # Nếu có user_id thì gán vào
        order_info.save()

        # Xử lý giỏ hàng: Nếu user đăng nhập, lấy từ CartInfo; nếu không, lấy từ session
        if user_id:
            cart_items = CartInfo.objects.filter(user_id=user_id)
        else:
            cart_items = request.session.get("guest_cart", {}).items()

        for item in cart_items:
            if user_id:
                cart = item
                goods = cart.goods
                count = cart.count
            else:
                goods_id, count = item
                goods = Goods.objects.get(pk=goods_id)

            if count <= goods.gkucun:
                goods.gkucun -= count
                goods.save()

                order_detail = OrderDetailInfo(
                    order=order_info,
                    goods=goods,
                    price=goods.gprice,
                    count=count,
                )
                order_detail.save()

                if user_id:
                    cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return HttpResponse("Out of Stock")

        if not user_id:
            request.session["guest_cart"] = {}  # Xóa giỏ hàng trong session sau khi đặt hàng

        data["ok"] = 1
        transaction.savepoint_commit(tran_id)

    except Exception as e:
        print("Order failed:", e)
        transaction.savepoint_rollback(tran_id)

    return JsonResponse(data)



@user_decorator.login
def pay(request):
    pass
