from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
import logging
import os

import requests

from df_cart.models import CartInfo
from df_user import user_decorator
from df_user.models import UserInfo
from df_goods.models import GoodsInfo
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, get_object_or_404
from django.db.models import Sum

from .models import OrderDetailInfo, OrderInfo

logger = logging.getLogger(__name__)


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
            total_price += int(cart.count) * int(cart.goods.gprice)
        total_count = cart_queryset.aggregate(Sum("count"))["count__sum"] or 0

    else:
        receiver = None  # Khách chưa có thông tin người nhận
        guest_cart = request.session.get("guest_cart", {})
        for goods_id, count in guest_cart.items():
            goods = GoodsInfo.objects.get(pk=goods_id)
            cart_items.append({"goods": goods, "count": count})
            total_price += int(count) * int(goods.gprice)
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

    print("context: ", context)

    return render(request, "df_order/place_order.html", context)


def send_order_to_telegram(order):
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    CHAT_ID = os.getenv("CHAT_ID", "")
    
    username = order.user.uname if order.user else "Guest"
    
    message = f"""
    🛒 **New Order Received!**  
    📦 Order ID: {order.oid}  
    👤 Customer: {username}  
    📍 Address: {order.oaddress}  
    📞 Phone: {order.ocontact}  
    💰 Total: {order.ototal}  
    ✅ Paid: {"Yes" if order.oIsPay else "No"}  
    🚚 Delivery: {"Yes" if order.oIsDelivery else "No"}
    """
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    response = requests.post(url, json=payload)
    return response.json()


@transaction.atomic
def order_handle(request):
    user_id = request.session.get("user_id")  # Can be None if guest
    address = request.POST.get("address", "").strip()
    receiver = request.POST.get("receiver", "").strip()
    phone = request.POST.get("contact", "").strip()
    total_str = request.POST.get("total", "0").strip()

    print(f"User ID: {user_id}, Address: {address}, Receiver: {receiver}, Phone: {phone}, Total: {total_str}")

    try:
        total = Decimal(total_str)
    except Exception:
        return JsonResponse({"error": "Invalid total amount"}, status=400)

    print("total: ", total)
    data = {}

    if user_id:
        user = UserInfo.objects.get(id=user_id)
    else:
        user = None
        
    try:
        order_info = OrderInfo(
            oid=f"{datetime.now().strftime('%Y%m%d%H%M%S')}{user_id or 0}",
            odate=datetime.now(),
            ototal=total,
            oaddress=address,
            ocontact=phone,
            oreceiver=receiver,
            user=user
        )
        order_info.save()

        # Get cart items
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
                goods = get_object_or_404(GoodsInfo, pk=goods_id)

            if count > goods.gkucun:
                return HttpResponse("Out of Stock", status=400)

            # Reduce stock and save
            goods.gkucun -= count
            goods.save()

            # Create order detail
            OrderDetailInfo.objects.create(
                order=order_info,
                goods=goods,
                price=goods.gprice,
                count=count,
            )

            if user_id:
                cart.delete()

        # Send order to Telegram
        send_order_to_telegram(order_info)

        # Clear guest cart
        if not user_id:
            request.session["guest_cart"] = {}
            data["ok"] = 0
        else:
            data["ok"] = 1
        return JsonResponse(data)

    except Exception as e:
        logger.error(f"Order failed: {e}", exc_info=True)
        return JsonResponse({"error": "Order processing failed"}, status=500)

@user_decorator.login
def pay(request):
    pass
