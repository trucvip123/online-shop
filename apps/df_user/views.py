import base64
from pathlib import Path
import re
import uuid

from decimal import Decimal, InvalidOperation
from hashlib import sha1

from df_cart.models import CartInfo
from df_goods.models import GoodsInfo, ProductImage, TypeInfo
from df_order.models import OrderInfo
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import (
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
    render,
    reverse,
)
from django.db.models import Sum

from . import user_decorator
from .models import GoodsBrowser, UserAddress, UserInfo


## This function is used to redirect the user to the resigter page.
def register(request):
    context = {
        "title": "Register",
    }
    return render(request, "df_user/register.html", context)


## This function is to handel the user's resigtration.
def register_handle(request):
    username = request.POST.get("user_name")
    password = request.POST.get("pwd")
    confirm_pwd = request.POST.get("confirm_pwd")
    fname = request.POST.get("fname")
    phone = request.POST.get("pnum")
    squestion = request.POST.get("squestion")
    sanswer = request.POST.get("sanswer")
    user_province = request.POST.get("province_name", "").strip()
    user_district = request.POST.get("district_name", "").strip()
    user_commune = request.POST.get("commune_name", "").strip()
    user_address = request.POST.get("address", "").strip()
    default_address = request.POST.get("is_default", True)

    # Check if the two passwords are the same.
    if password != confirm_pwd:
        return redirect("/user/register/")
    # password encryption
    s1 = sha1()
    s1.update(password.encode("utf8"))
    encrypted_pwd = s1.hexdigest()

    # Create UserInfo instance
    user = UserInfo.objects.create(
        uname=username,
        upwd=encrypted_pwd,
        ufullname=fname,
        uphone=phone,
        uquestion=squestion,
        uanswer=sanswer,
    )
    # Create UserAddress instance
    UserAddress.objects.create(
        user=user,
        uprovince=user_province,
        udistrict=user_district,
        ucommune=user_commune,
        uaddress_detail=user_address,
        default_address_flg=default_address,
    )

    context = {
        "title": "Sign up",
        "username": username,
    }
    return render(request, "df_user/login.html", context)


# verfiy whether the username exists
def register_exist(request):
    username = request.GET.get("uname")
    count = UserInfo.objects.filter(uname=username).count()
    return JsonResponse({"count": count})


def merge_guest_cart(request):
    user_id = request.session.get("user_id")
    guest_uid = f"guest_{request.session.session_key}"

    guest_cart_items = CartInfo.objects.filter(user_id=guest_uid)

    for item in guest_cart_items:
        cart, created = CartInfo.objects.get_or_create(
            user_id=user_id, 
            goods_id=item.goods_id, 
            defaults={"count": item.count}
        )
        if not created:
            cart.count += item.count
            cart.save()

        # Xóa giỏ hàng của khách vãng lai sau khi hợp nhất
        item.delete()


def login(request):
    uname = request.COOKIES.get("uname", "")
    context = {
        "title": "Login",
        "error_name": 0,
        "error_pwd": 0,
        "uname": uname,
    }
    return render(request, "df_user/login.html", context)


def login_handle(request):
    uname = request.POST.get("username")
    upwd = request.POST.get("pwd")
    jizhu = request.POST.get("jizhu", 0)
    # get the request information and retrieve the information from the form
    users = UserInfo.objects.filter(uname=uname)
    # use ORM to get the users information
    if (
        len(users) == 1
    ):  # if the users exits, convert the pwd user input into sha-1 code
        s1 = sha1()
        s1.update(upwd.encode("utf8"))

        if s1.hexdigest() == users[0].upwd:  # if the pwd matched
            url = request.COOKIES.get("url", "/")
            red = HttpResponseRedirect(url)

            if jizhu != 0:
                red.set_cookie("uname", uname)
            else:
                red.set_cookie("uname", "", max_age=-1)
            request.session["user_id"] = users[0].id
            request.session["user_name"] = uname

            # 🔥 Merge guest cart after login
            merge_guest_cart(request)

            return red
        else:  # if the code doesn't match
            context = {
                "title": "Login",
                "error_name": 0,
                "error_pwd": 1,
                "uname": uname,
                "upwd": upwd,
            }
            return render(request, "df_user/login.html", context)
    else:
        context = {
            "title": "Login",
            "error_name": 1,
            "error_pwd": 0,
            "uname": uname,
            "upwd": upwd,
        }
        return render(request, "df_user/login.html", context)


def logout(request):  # logout
    request.session.flush()  # clear all sessions
    return redirect(reverse("df_goods:index"))


# view history
@user_decorator.login
def info(request):  # user center
    username = request.session.get("user_name")
    user = UserInfo.objects.filter(uname=username).first()
    browser_goods = (
        GoodsBrowser.objects.filter(user=user)
        .select_related("good")
        .order_by("-browser_time")
    )
    goods_list = []
    if browser_goods:
        goods_list = [browser_good.good for browser_good in browser_goods]
        explain = "Recently views"
    else:
        explain = "Relevant views"

    addresses = UserAddress.objects.filter(user=user).order_by(
        "-default_address_flg", "id"
    )

    context = {
        "title": "User Center",
        "page_name": 1,
        "user_full_name": user.ufullname,
        "user_phone": user.uphone,
        "user_name": username,
        "goods_list": goods_list,
        "explain": explain,
        "address_list": addresses,
    }

    return render(request, "df_user/user_center_info.html", context)


@user_decorator.login
def info_reset(request):
    user_name = request.session.get("user_name")

    # Kiểm tra user có tồn tại không
    user = UserInfo.objects.filter(uname=user_name)
    if not user.exists():
        return render(
            request,
            "df_user/user_center_info.html",
            {
                "title": "change the information",
                "error": "User not found.",
            },
        )

    # Lấy thông tin từ request (có giá trị mặc định tránh lỗi)
    user_full_name = request.POST.get("fullname", "").strip()
    user_phone = request.POST.get("phone", "").strip()

    # Cập nhật thông tin user
    user.update(
        ufullname=user_full_name,
        uphone=user_phone,
    )

    # Lấy lại user sau khi update
    user = user.first()

    # Lấy lịch sử duyệt hàng
    browser_goods = GoodsBrowser.objects.filter(user=user).order_by("-browser_time")
    goods_list = (
        [browser_good.good for browser_good in browser_goods]
        if browser_goods.exists()
        else []
    )
    explain = "Recently views" if goods_list else "Relevant views"
    addresses = UserAddress.objects.filter(user=user)

    context = {
        "title": "change the information",
        "success": 1,
        "script": "alert",
        "page_name": 1,
        "user_full_name": user.ufullname,
        "user_phone": user.uphone,
        "user_name": user.uname,
        "goods_list": goods_list,
        "explain": explain,
        "address_list": addresses,
    }

    return render(request, "df_user/user_center_info.html", context)


@user_decorator.login
def insert_user_address(request):
    user_name = request.session.get("user_name")

    user = get_object_or_404(UserInfo, uname=user_name)

    # Get address data from the form
    user_province = request.POST.get("province_name", "").strip()
    user_district = request.POST.get("district_name", "").strip()
    user_commune = request.POST.get("commune_name", "").strip()
    user_address = request.POST.get("address", "").strip()
    default_address = request.POST.get("is_default", False)

    if default_address == "on":
         # Set all existing addresses' default_address_flg to False
        UserAddress.objects.filter(user=user).update(default_address_flg=False)
        default_address = True

    # Create a new product
    address = UserAddress.objects.create(
        user=user,
        uprovince=user_province,
        udistrict=user_district,
        ucommune=user_commune,
        uaddress_detail=user_address,
        default_address_flg=default_address,
    )

    # Lấy lịch sử duyệt hàng
    browser_goods = GoodsBrowser.objects.filter(user=user).order_by("-browser_time")
    goods_list = (
        [browser_good.good for browser_good in browser_goods]
        if browser_goods.exists()
        else []
    )

    addresses = UserAddress.objects.filter(user=user).order_by(
        "-default_address_flg", "id"
    )
    context = {
        "title": "change the information",
        "success": 1,
        "script": "alert",
        "page_name": 1,
        "user_full_name": user.ufullname,
        "user_phone": user.uphone,
        "user_name": user.uname,
        "goods_list": goods_list,
        "address_list": addresses,
    }
    return render(request, "df_user/user_center_info.html", context)

def edit_user_address(request):
    user_name = request.session.get("user_name")

    user = get_object_or_404(UserInfo, uname=user_name)

    # Get address data from the form
    user_province = request.POST.get("province_name", "").strip()
    user_district = request.POST.get("district_name", "").strip()
    user_commune = request.POST.get("commune_name", "").strip()
    user_address = request.POST.get("address", "").strip()
    default_address = request.POST.get("is_default", False)

    # Set all existing addresses' default_address_flg to False
    UserAddress.objects.filter(user=user).update(default_address_flg=False)

    if default_address == "on":
        default_address = True
    # Create a new product
    address = UserAddress.objects.create(
        user=user,
        uprovince=user_province,
        udistrict=user_district,
        ucommune=user_commune,
        uaddress_detail=user_address,
        default_address_flg=default_address,
    )

    # Lấy lịch sử duyệt hàng
    browser_goods = GoodsBrowser.objects.filter(user=user).order_by("-browser_time")
    goods_list = (
        [browser_good.good for browser_good in browser_goods]
        if browser_goods.exists()
        else []
    )

    addresses = UserAddress.objects.filter(user=user).order_by(
        "-default_address_flg", "id"
    )

    context = {
        "title": "change the information",
        "success": 1,
        "script": "alert",
        "page_name": 1,
        "user_full_name": user.ufullname,
        "user_phone": user.uphone,
        "user_name": user.uname,
        "goods_list": goods_list,
        "address_list": addresses,
    }
    return render(request, "df_user/user_center_info.html", context)


def delete_user_address(request, address_id):
    try:
        address = UserAddress.objects.get(pk=int(address_id))
        address.delete()
        return JsonResponse({'success': True})
    except Exception:
        return JsonResponse({'success': False, 'error': 'Address not found'})
    
@user_decorator.login
def order(request, index):
    user_id = request.session["user_id"]
    orders_list = OrderInfo.objects.filter(user_id=int(user_id)).order_by("-odate")
    paginator = Paginator(orders_list, 2)
    page = paginator.page(int(index))
    context = {
        "paginator": paginator,
        "page": page,
        # 'orders_list':orders_list,
        "title": "User Center",
        "page_name": 1,
    }
    return render(request, "df_user/user_center_order.html", context)


## This function is to handle the reset information.
def reset_handle(request):
    # question=request.POST.get('security_question')
    answer = request.POST.get("security_answer")
    password = request.POST.get("pwd")
    confirm_password = request.POST.get("confirm_pwd")
    uname = request.session.get("user_name")
    users = UserInfo.objects.filter(uname=uname)

    security_answer = users[0].uanswer
    if password != confirm_password:
        return redirect("/user/register/")
    if answer == security_answer:
        s1 = sha1()
        s1.update(password.encode("utf8"))
        encrypted_pwd = s1.hexdigest()
        users.update(upwd=encrypted_pwd)
        context = {"title": "the security answer is incorrect", "answer_error": 0}
        return render(request, "df_user/login.html", context)

    else:
        context = {
            "title": "the security answer is incorrect",
            "answer_error": 1,
            "security_question": users[0].uquestion,
            "username": users[0].uname,
        }
        return render(request, "df_user/find_password.html", context)


## This funtion is to model is ensure the username provided by the user exists.
def find_password(request):
    uname = request.POST.get("user_name")
    users = UserInfo.objects.filter(uname=uname)
    if (
        len(users) == 1
    ):  ## If the user exists, the user will be redirected to the reset page.

        url = "df_user/find_password.html"
        red = HttpResponseRedirect(url)

        request.session["user_id"] = users[0].id
        request.session["user_name"] = uname
        context = {
            "title": "Reset the password",
            "username": users[0].uname,
            # 'security_question':users[0].usecurity_question,
            "security_question": users[0].uquestion,
            # 'security_answer':users[0].usecurity_answer,
        }
        return render(request, "df_user/find_password.html", context)

    else:
        context = {
            "title": "Login",
            "error_name": 1,
            "error_pwd": 0,
            "blanl_name": 0,
            "uname": uname,
        }
        return render(request, "df_user/forgetPassword.html", context)


## This function is to redirect the user to the reset page.
def forget_password(request):
    uname = request.COOKIES.get("uname", "")
    context = {
        "title": "Login",
        "error_name": 0,
        "error_pwd": 0,
        "uname": uname,
    }
    return render(request, "df_user/forgetPassword.html", context)


## The method decorator is applied here to ensure the user is logged in.
## This function is to redirect the user to redirect the user to the change password page in the user center.
@user_decorator.login
def site(request):
    return render(request, "df_user/user_center_site.html")


## This function is to handle the change password request from the user.
def site_handle(request):
    user = UserInfo.objects.get(id=request.session["user_id"])
    if request.method == "POST":
        pwd = request.POST.get("pwd")
        confirm_pwd = request.POST.get("confirm_pwd")
        if pwd == confirm_pwd:

            # password encryption
            s1 = sha1()
            s1.update(pwd.encode("utf8"))
            user.upwd = s1.hexdigest()

            user.save()
            return render(request, "df_user/user_center_site.html", {"success": 1})
        else:
            return redirect("df_user/user_center_site.html")
    return render(request, "df_user/user_center_site.html", {"success": 1})


@user_decorator.login
def add_product(request):
    context = {
        "title": "Add Product",
        "types": TypeInfo.objects.all(),
    }
    return render(request, "df_user/user_center_add_product.html", context)


@user_decorator.login
def edit_product(request):
    context = {
        "title": "Edit Product",
        "types": TypeInfo.objects.all(),
    }
    return render(request, "df_user/user_center_edit_product.html", context)


# Define a decorator to check if the user is an admin
def admin_required(user):
    return user.is_authenticated and user.is_staff


# @user_passes_test(admin_required)
def add_product_handle(request):
    if request.method == "POST":
        # Get product data from the form
        name = request.POST.get("product_name")
        brand = request.POST.get("brand_name")
        price = request.POST.get("price")
        price_old = request.POST.get("price_old")
        description = request.POST.get("description")
        param = request.POST.get("parameters")
        type_id = request.POST.get("product_type")
        stock = request.POST.get("stock")

        # Fetch the TypeInfo instance based on type_id
        category = get_object_or_404(TypeInfo, id=type_id)
        price_decimal = Decimal(price)

        # Check if a product with the same title already exists
        if GoodsInfo.objects.filter(gtitle=name).exists():
            return render(
                request,
                "df_user/user_center_add_product.html",
                {
                    "title": "Add Product",
                    "types": TypeInfo.objects.all(),
                    "error": "A product with this title already exists.",
                },
            )

        # Create a new product
        product = GoodsInfo.objects.create(
            gtitle=name,
            gprice=price_decimal,
            gprice_old=price_old,
            gcontent=description,
            gparam=param,
            gtype=category,
            gkucun=stock,
            gbrand=brand,
        )
        # Handle multiple images
        images = request.FILES.getlist("image")
        for image in images:
            ProductImage.objects.create(product=product, image_path=image)

        return redirect(f"/{product.pk}")

    return render(request, "df_user/user_center_add_product.html")


def cart_count(request):
    if "user_id" in request.session:
        return CartInfo.objects.filter(user_id=request.session["user_id"]).aggregate(
            Sum("count")
        )["count__sum"]
    else:
        return 0


# @user_passes_test(admin_required)
def edit_product_handle(request):
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=405)

    # Extract and validate inputs
    product_id = request.POST.get("product_id", "").strip()
    name = request.POST.get("product_name", "").strip()
    brand = request.POST.get("brand_name", "").strip()
    price = request.POST.get("price", "").strip()
    price_old = request.POST.get("price_old", "").strip()
    description = request.POST.get("description", "").strip()
    parameter = request.POST.get("parameter", "").strip()
    stock = request.POST.get("stock", "").strip()

    if not product_id.isdigit():
        return HttpResponse("Invalid product ID", status=400)

    # Check if editing an existing product
    product = get_object_or_404(GoodsInfo, id=int(product_id)) if product_id else None

    if not product:
        return HttpResponse("Product not found", status=404)

    try:
        price_decimal = Decimal(price)
        price_old_decimal = Decimal(price_old)
    except (InvalidOperation, TypeError):
        return HttpResponse("Invalid price format", status=400)

    # Update product details
    product.gtitle = name
    product.gprice = price_decimal
    product.gprice_old = price_old_decimal
    product.gcontent = description
    product.gparam = parameter
    product.gkucun = stock
    product.gbrand = brand
    product.save()

    # Delete all existing images of the product
    existing_images = ProductImage.objects.filter(product=product)
    # Handle multiple images
    image_data_list = request.POST.getlist("image_urls[]")

    # Identify images to delete
    delete_img_ls = {
        img.image_path.name
        for img in existing_images
        if all(
            Path(img.image_path.name).as_posix() not in img_data
            for img_data in image_data_list
        )
    }
    # Delete images from storage and database
    for image in delete_img_ls:
        if default_storage.exists(image):
            default_storage.delete(image)  # Deletes from configured storage backend
        ProductImage.objects.filter(image_path=image).delete()

    # Handle new images
    insert_img_ls = [img_data for img_data in image_data_list if "base64" in img_data]

    for image_data in insert_img_ls:
        format_img, imgstr = image_data.split(";base64,")
        ext = format_img.split("/")[-1]
        img_data = base64.b64decode(imgstr)

        image_name = f"{uuid.uuid4()}.{ext}"
        image_path = f"df_goods/images/{image_name}"

        # Save image using Django's storage backend
        file_path = default_storage.save(image_path, ContentFile(img_data))

        # Save reference in database
        ProductImage.objects.create(product=product, image_path=file_path)

    return redirect(f"/{product_id}")


def get_product_details_by_id(request):
    image_urls = []
    product_id = request.GET.get("product_id")

    try:
        product = GoodsInfo.objects.get(pk=int(product_id))
        imgs = ProductImage.objects.filter(product=product)
        if imgs.exists():
            image_urls = ["/media/" + str(img.image_path) for img in imgs]
        data = {
            "product_name": product.gtitle,
            "product_type": product.gtype.ttitle,
            "brand_name": product.gbrand,
            "price": str(product.gprice),
            "price_old": str(product.gprice_old),
            "parameter": product.gparam,
            "description": product.gcontent,
            "stock": product.gkucun,
            "image_urls": image_urls,
        }
    except GoodsInfo.DoesNotExist:
        data = {"error": "Product not found"}

    return JsonResponse(data)


def add_new_type(request):
    if request.method == "POST":
        new_type = request.POST.get("new_product_type")
        new_type_name = request.POST.get("new_product_type_name")
        if new_type:
            # Check if the new_type already exists in the TypeInfo table
            if TypeInfo.objects.filter(ttitle=new_type).exists():
                return HttpResponse("This product type already exists.")
            else:
                TypeInfo.objects.create(ttitle=new_type, ntitle=new_type_name)
                return render(
                    request, "df_user/user_center_manage_type.html", {"success": 1}
                )
    return HttpResponse("Invalid request method.")


def delete_type(request):
    if request.method == "POST":
        type_id = request.POST.get("product_type_delete")
        if type_id:
            try:
                type_to_delete = TypeInfo.objects.get(id=type_id)
                type_to_delete.delete()
                return render(
                    request, "df_user/user_center_manage_type.html", {"success": 1}
                )
            except TypeInfo.DoesNotExist:
                return HttpResponse("The specified type does not exist.")
    return HttpResponse("Invalid request method.")


def edit_type(request):
    if request.method == "POST":
        old_type_name = request.POST.get("product_type_old")
        new_type_name = request.POST.get("product_type_new")

        if not old_type_name or not new_type_name:
            return JsonResponse(
                {"error": "Type ID and new type name are required."}, status=400
            )

        try:
            type_to_edit = TypeInfo.objects.get(ttitle=old_type_name)
            type_to_edit.ttitle = new_type_name
            type_to_edit.save()
            return render(
                request, "df_user/user_center_manage_type.html", {"success": 1}
            )
        except TypeInfo.DoesNotExist:
            return JsonResponse(
                {"error": "The specified type does not exist."}, status=404
            )
        except Exception as e:
            return JsonResponse(
                {"error": f"An unexpected error occurred: {str(e)}"}, status=500
            )
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


def manage_type(request):
    return render(request, "df_user/user_center_manage_type.html")
