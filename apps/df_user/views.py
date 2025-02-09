from decimal import Decimal
from hashlib import sha1

from df_cart.models import CartInfo
from df_goods.models import GoodsInfo, ProductImage, TypeInfo
from df_order.models import OrderInfo
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import (
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
    render,
    reverse,
)
from django.core.files.storage import FileSystemStorage

from . import user_decorator
from .models import GoodsBrowser, UserInfo


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
    email = request.POST.get("email")
    fname = request.POST.get("fname")
    phone = request.POST.get("pnum")
    squestion = request.POST.get("squestion")
    sanswer = request.POST.get("sanswer")

    # Check if the two passwords are the same.
    if password != confirm_pwd:
        return redirect("/user/register/")
    # password encryption
    s1 = sha1()
    s1.update(password.encode("utf8"))
    encrypted_pwd = s1.hexdigest()

    # create object in the database
    UserInfo.objects.create(
        uname=username,
        upwd=encrypted_pwd,
        uemail=email,
        ufullname=fname,
        uphone=phone,
        uquestion=squestion,
        uanswer=sanswer,
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

    context = {
        "title": "User Center",
        "page_name": 1,
        "user_full_name": user.ufullname,
        "user_email": user.uemail,
        "user_phone": user.uphone,
        "user_name": username,
        "user_address": user.uaddress,
        "goods_list": goods_list,
        "explain": explain,
    }
    return render(request, "df_user/user_center_info.html", context)


## The method decorator is applied here.
## If the user is not logged in, the user will be redirected to the login page.
## this function is to redirect user to the user center reset information page.


@user_decorator.login
def info_reset(request):
    user_name = request.session.get("user_name")
    user = UserInfo.objects.filter(uname=user_name)
    user_full_name = request.POST.get("fullname")
    user_email = request.POST.get("email")
    user_phone = request.POST.get("phone")
    browser_goods = GoodsBrowser.objects.filter(user__in=user).order_by("-browser_time")
    goods_list = []
    if browser_goods:
        goods_list = [browser_good.good for browser_good in browser_goods]
        explain = "Recently views"
    else:
        explain = "Relevant views"
    user.update(
        ufullname=user_full_name,
        # upwd=encrypted_pwd,
        uemail=user_email,
        uphone=user_phone,
        # uaddress=user_address,
    )
    user = UserInfo.objects.filter(uname=user_name).first()
    context = {
        "title": "change the information",
        "success": 1,
        "script": "alert",
        "page_name": 1,
        "user_full_name": user.ufullname,
        "user_email": user.uemail,
        "user_phone": user.uphone,
        "user_name": user_name,
        "goods_list": goods_list,
        "explain": explain,
    }
    return render(request, "df_user/user_center_info.html", context)


## The method decorator is applied here.
## If the user is not logged in, the user will be redirected to the login page.
## This function is for user to check their previous orders
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
            "title": "reset the password",
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
        price = request.POST.get("price")
        description = request.POST.get("description")
        type_id = request.POST.get("product_type")  # Get selected type ID from form

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
            gcontent=description,
            gtype=category,
        )
        # Handle multiple images
        images = request.FILES.getlist("image")
        print("images:", images)

        for i, image in enumerate(images):
            fs = FileSystemStorage()
            print(image.name, image)
            ProductImage.objects.create(product=product, image_path=images[i])

        goods = GoodsInfo.objects.get(gtitle=name)
        news = goods.gtype.goodsinfo_set.order_by("-id")[0:2]

        context = {
            "goods": goods,
            "news": news,
        }
        # return render(request, "df_goods/detail.html", context)
        return render(request, "df_user/user_center_add_product.html", {"success": 1})

    return render(request, "df_user/user_center_add_product.html")


def cart_count(request):
    if "user_id" in request.session:
        return CartInfo.objects.filter(user_id=request.session["user_id"]).count
    else:
        return 0


# @user_passes_test(admin_required)
def edit_product_handle(request):
    product_id = request.GET.get("product_id")
    print("product_id:", product_id)

    # Check if editing an existing product
    if product_id:
        product = get_object_or_404(GoodsInfo, id=product_id)
    else:
        product = None

    if request.method == "POST":
        # Get product data from the form
        name = request.POST.get("product_name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        category = request.POST.get("product_type")  # Get selected type ID from form
        # image_path = request.FILES.get("image", None)

        price_decimal = Decimal(price)

        if product:
            # Update existing product
            product.gtitle = name
            product.gprice = price_decimal
            product.gcontent = description
            # product.gpic = image_path
            product.save()

            # Handle multiple images
            images = request.FILES.getlist("image")
            for i, image in enumerate(images):
                fs = FileSystemStorage()
                # fs.save(image.name, image)
                ProductImage.objects.create(product=product, image_path=images[i])

            goods = GoodsInfo.objects.get(pk=int(product_id))
            news = goods.gtype.goodsinfo_set.order_by("-id")[0:2]

            context = {
                "title": goods.gtype.ttitle,
                "guest_cart": 1,
                "cart_num": cart_count(request),
                "goods": goods,
                "news": news,
                "id": product_id,
            }
            return render(request, "df_goods/detail.html", context)

    context = {
        "title": "Add Product",
        "product": product,  # Pass product data if editing
        "types": TypeInfo.objects.all(),
    }
    return render(request, "df_user/user_center_edit_product.html", context)


def get_product_details_by_id(request):
    product_id = request.GET.get("product_id")
    print("product_id:", product_id)
    try:
        product = GoodsInfo.objects.get(pk=int(product_id))
        data = {
            "product_name": product.gtitle,
            "product_type": product.gtype.ttitle,
            "price": str(product.gprice),
            "description": product.gcontent,
            "stock": product.gkucun,
            "image_url": product.gpic.url if product.gpic else "",
        }
        print("data:", data)
    except GoodsInfo.DoesNotExist:
        data = {"error": "Product not found"}

    return JsonResponse(data)


def add_new_type(request):
    if request.method == "POST":
        new_type = request.POST.get("new_product_type")
        if new_type:
            # Check if the new_type already exists in the TypeInfo table
            if TypeInfo.objects.filter(ttitle=new_type).exists():
                return HttpResponse("This product type already exists.")
            else:
                TypeInfo.objects.create(ttitle=new_type)
                return render(
                    request, "df_user/user_center_manage_type.html", {"success": 1}
                )
    return HttpResponse("Invalid request method.")


def delete_type(request):
    if request.method == "POST":
        type_id = request.POST.get("product_type_delete")
        print("type_id:", type_id)
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
