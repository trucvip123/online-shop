from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse

from hashlib import sha1

from .models import GoodsBrowser
from . import user_decorator
from .models import UserInfo
from df_order.models import OrderInfo


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
    browser_goods = GoodsBrowser.objects.filter(user=user).order_by("-browser_time")
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
    print(len(users))
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
