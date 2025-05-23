import math
import re
from df_cart.models import CartInfo
from df_user.models import GoodsBrowser
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Sum

from .models import GoodsInfo, TypeInfo


# the products to display on the main page
def index(request):
    # check the 4 new arrival product of category
    typelist = TypeInfo.objects.all()
    goodsinfo = GoodsInfo.objects.all()

    newest_products = goodsinfo.order_by("-id")[:10]

    den_chum_instance = TypeInfo.objects.filter(ttitle='den-chum').first()
    den_chum_type = den_chum_instance.goodsinfo_set.order_by("-id")[:10]
    
    may_lanh_instance = TypeInfo.objects.filter(ttitle='may-lanh').first()
    may_lanh_type = may_lanh_instance.goodsinfo_set.order_by("-id")[:10]
    
    quat_dieu_hoa_instance = TypeInfo.objects.filter(ttitle='quat-dieu-hoa').first()
    quat_dieu_hoa_type = quat_dieu_hoa_instance.goodsinfo_set.order_by("-id")[:10]

    noi_chien_khong_dau_instance = TypeInfo.objects.filter(ttitle='noi-chien-khong-dau').first()
    noi_chien_khong_dau_type = noi_chien_khong_dau_instance.goodsinfo_set.order_by("-id")[:10]

    context = {
        "title": "Mua bán điện tử, điện lạnh, điện gia dụng",
        "cart_num": cart_count(request),
        "guest_cart": 1,
        "newest_products": newest_products,
        "den_chum_type": den_chum_type,
        "may_lanh_type": may_lanh_type,
        "quat_dieu_hoa_type": quat_dieu_hoa_type,
        "noi_chien_khong_dau_type": noi_chien_khong_dau_type,
    }
    return render(request, "df_goods/index.html", context)

def good_list(request, category, pindex, sort, brand=None):
    # Get product category info
    typeinfo = TypeInfo.objects.get(ttitle=category)
    
    # Get the latest 4 products in this category
    news = typeinfo.goodsinfo_set.order_by("-id")[0:4]

    goods_list = []

    # Get cart info
    cart_num, guest_cart = 0, 0
    try:
        user_id = request.session["user_id"]
    except:
        user_id = None
        
    if user_id:
        guest_cart = 1
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).aggregate(
            Sum("count")
        )["count__sum"]
        
        
    # Base query for filtering goods
    query = GoodsInfo.objects.filter(gtype_id=int(typeinfo.id))
    
    # Apply brand filter if provided
    if brand:
        query = query.filter(gbrand__icontains=brand)  # Case-insensitive contains match for brand

    # Apply sorting
    if sort == "1":  # default(from the newest)
        goods_list = query.order_by("-id")
    elif sort == "2":  # price descending
        goods_list = query.order_by("-gprice")
    elif sort == "3":  # hot
        goods_list = query.order_by("-gclick")
    elif sort == "4":  # price ascending
        goods_list = query.order_by("gprice")
    
    # Paginator
    paginator = Paginator(goods_list, 20)
    # return page object
    page = paginator.page(int(pindex))

    image_category = None
    if page.object_list and len(page.object_list) > 0:
        first_product = page.object_list[0]
        if first_product.images.all().exists():
            image_category = first_product.images.all()[0].image_path

    # Xác định image type
    image_type = 'jpeg'  # default
    if image_category:
        if hasattr(image_category, 'name'):
            ext = image_category.name.split('.')[-1].lower()
            if ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                image_type = ext
                if ext == 'jpg':
                    image_type = 'jpeg'

    print("image_category:", image_category)

    context = {
        "title": typeinfo.ntitle,
        "guest_cart": guest_cart,
        "cart_num": cart_count(request),
        "page": page,
        "paginator": paginator,
        "typeinfo": typeinfo,
        "sort": sort,
        "news": news,
        "selected_brand": brand,
        "image_category": image_category,
        "image_type": image_type,
    }
    return render(request, "df_goods/list.html", context)

def convert_urls_to_images(text):
    url_pattern = re.compile(r"(https?://\S+\.(?:jpg|jpeg|png|gif))")
    return url_pattern.sub(
        r'<img src="\1" alt="Image" style="max-width: 100%; height: auto; margin-left: 10px; display: flex">',
        text,
    )

def round_up_to_even(number):
    rounded = math.ceil(number)  # Làm tròn lên
    return rounded if rounded % 2 == 0 else rounded + 1 

def detail(request, gid):
    good_id = gid
    goods = GoodsInfo.objects.get(pk=int(good_id))
    goods.gclick = goods.gclick + 1  # clicks
    goods.save()

    # Apply the render_images filter to the goods.gcontent field
    # goods.gcontent = convert_urls_to_images(goods.gcontent)

    news = goods.gtype.goodsinfo_set.order_by("-id")[0:round_up_to_even(len(goods.gparam)/200)]
    context = {
        "ttitle": goods.gtype.ttitle,
        "ntitle": goods.gtype.ntitle,
        "guest_cart": 1,
        "cart_num": cart_count(request),
        "goods": goods,
        "news": news,
        "id": good_id,
        "discount": ((goods.gprice_old - goods.gprice) / goods.gprice_old) * 100,
    }
    response = render(request, "df_goods/detail.html", context)

    if "user_id" in request.session:
        user_id = request.session["user_id"]
        try:
            browsed_good = GoodsBrowser.objects.get(
                user_id=int(user_id), good_id=int(good_id)
            )
        except Exception:
            browsed_good = None
        if browsed_good:
            from datetime import datetime

            browsed_good.browser_time = datetime.now()
            browsed_good.save()
        else:
            GoodsBrowser.objects.create(user_id=int(user_id), good_id=int(good_id))
            browsed_goods = GoodsBrowser.objects.filter(user_id=int(user_id))
            browsed_good_count = browsed_goods.count()
            if browsed_good_count > 5:
                ordered_goods = browsed_goods.order_by("-browser_time")
                for _ in ordered_goods[5:]:
                    _.delete()
    return response


def cart_count(request):
    uid = request.session.get("user_id")

    if uid:  # Nếu user đã đăng nhập -> lấy từ DB
        carts = CartInfo.objects.filter(user_id=uid)
        count = carts.aggregate(Sum("count"))["count__sum"] or 0
    else:  # Nếu là khách -> lấy từ session
        guest_cart = request.session.get("guest_cart", {})
        count = sum(guest_cart.values())
        carts = []
    return count


# the search function
def ordinary_search(request):

    from django.db.models import Q

    search_keywords = request.GET.get("q", "")
    pindex = request.GET.get("page", 1)
    search_status = 1
    cart_num, guest_cart = 0, 0

    try:
        user_id = request.session["user_id"]
    except:
        user_id = None

    if user_id:
        guest_cart = 1
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).aggregate(
            Sum("count")
        )["count__sum"]

    goods_list = GoodsInfo.objects.filter(
        Q(gtitle__icontains=search_keywords)
        | Q(gcontent__icontains=search_keywords)
        | Q(gjianjie__icontains=search_keywords)
        | Q(gparam__icontains=search_keywords)
        | Q(gbrand__icontains=search_keywords)
        | Q(gvideo_url__icontains=search_keywords)
    ).order_by("gclick")

    if goods_list.count() == 0:
        # search result is empty, return some recommendation
        search_status = 0
        goods_list = GoodsInfo.objects.all().order_by("gclick")[:4]
    # paginator function to split the page when the products are too many
    paginator = Paginator(goods_list, 12)
    page = paginator.page(int(pindex))

    context = {
        "title": "Search list",
        "search_status": search_status,
        "guest_cart": guest_cart,
        "cart_num": cart_num,
        "page": page,
        "paginator": paginator,
        "query": search_keywords,
    }
    return render(request, "df_goods/ordinary_search.html", context)
