from df_user import user_decorator
from django.http import JsonResponse
from django.shortcuts import redirect, render, reverse
from django.db.models import Sum
from django.shortcuts import (
    get_object_or_404,
)
import logging

from .models import *

logger = logging.getLogger(__name__)


def user_cart(request):
    uid = request.session.get("user_id")
    carts = []
    total_count = 0

    if uid:  # Nếu user đã đăng nhập -> lấy từ DB
        carts = CartInfo.objects.filter(user_id=uid)
        total_count = carts.aggregate(Sum("count"))["count__sum"] or 0
    else:  # Nếu là khách -> lấy từ session
        guest_cart = request.session.get("guest_cart", {})
        print("guest_cart:", guest_cart)

        # Duyệt qua từng sản phẩm trong giỏ hàng session và lấy thông tin từ DB
        for goods_id, count in guest_cart.items():
            try:
                goods = GoodsInfo.objects.get(pk=goods_id)
                carts.append({"goods": goods, "count": count})
            except GoodsInfo.DoesNotExist:
                pass  # Nếu sản phẩm không tồn tại, bỏ qua

        total_count = sum(guest_cart.values())

    context = {
        "title": "Shopping Cart",
        "page_name": 1,
        "carts": carts,  # Bây giờ danh sách này có đầy đủ thông tin sản phẩm
        "cart_num": total_count,
    }
    return render(request, "df_cart/cart.html", context)


def add(request, gid, count):
    gid, count = gid, int(count)
    uid = request.session.get("user_id")

    if uid:  # Nếu user đã đăng nhập, lưu vào DB
        cart, created = CartInfo.objects.get_or_create(
            user_id=uid,
            goods_id=gid,
            defaults={"count": count},
        )
        if not created:
            cart.count += count
            cart.save()

        cart_count = CartInfo.objects.filter(user_id=uid).aggregate(Sum("count"))["count__sum"]
    
    else:  # Nếu là khách, lưu vào session
        guest_cart = request.session.get("guest_cart", {})
        guest_cart[gid] = guest_cart.get(gid, 0) + count
        request.session["guest_cart"] = guest_cart
        request.session.modified = True  # Bắt buộc Django lưu session ngay lập tức
        cart_count = sum(guest_cart.values())

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"count": cart_count})
    
    context = {"cart_num": cart_count}
    return render(request, "df_cart/cart.html", context)

def edit(request, gid, count):
    data = {}

    try:
        count = int(count)
        if count < 1:
            return JsonResponse({"error": "Quantity must be at least 1"}, status=400)

        uid = request.session.get("user_id")
        
        if uid:  # Logged-in user
            cart = get_object_or_404(CartInfo, goods_id=gid, user_id=uid)
            cart.count = count
            cart.save()
        else:  # Guest user
            guest_cart = request.session.get("guest_cart", {})

            if str(gid) in guest_cart:
                guest_cart[str(gid)] = count
                request.session["guest_cart"] = guest_cart
            else:
                return JsonResponse({"error": "Item not found in guest cart"}, status=404)

        data["count"] = count
        return JsonResponse(data)

    except ValueError:
        return JsonResponse({"error": "Invalid input"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# @user_decorator.login
def delete(request, gid):
    data = {"ok": 0}  # Default response
    try:
        uid = request.session.get("user_id")
        
        if uid:  # Logged-in user
            cart = get_object_or_404(CartInfo, goods_id=gid, user_id=uid)
            cart.delete()
            data["ok"] = 1
        else:  # Guest user
            guest_cart = request.session.get("guest_cart", {})
            if str(gid) in guest_cart:
                del guest_cart[str(gid)]  # Remove item from guest cart
                request.session["guest_cart"] = guest_cart  # Update session
                request.session.modified = True  # Ensure session saves
                data["ok"] = 1

    except Exception as e:
        logger.error(f"Error deleting item {gid}: {e}")

    return JsonResponse(data)
