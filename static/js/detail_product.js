$(document).ready(function () {
    $(".buy_btn").click(function () {
        num = parseInt($('.num_show').val());
        $.get('/cart/add{{ goods.id }}_' + num + '/', function (data) {
            $('#show_count').text(data.count);
        });
        location.href = "/cart/";
    });

    $('#add_cart').click(function () {
        var $add_x = $('#add_cart').offset().top;
        var $add_y = $('#add_cart').offset().left;
        var $to_x = $('#show_count').offset().top;
        var $to_y = $('#show_count').offset().left;

        $(".add_jump").css({ 'left': $add_y + 80, 'top': $add_x + 10, 'display': 'block' });

        // { #check login or not# };
        if ($('.login_btn').text().indexOf('Login') >= 0) {
            alert('Please login first');
            location.href('/user/login/');
            return;
        }

        // { #add to cart animation# }
        $(".add_jump").stop().animate({
            'left': $to_y + 7,
            'top': $to_x + 7
        },
            "fast", function () {
                $(".add_jump").fadeOut('fast', function () {
                    count = $('.num_show').val();
                    $('#show_count').html(count);
                });
            });

        num = parseInt($('.num_show').val());
        $.get('/cart/add{{ goods.id }}_' + num + '/', function (data) {
            $('#show_count').text(data.count);

        });
    });

    $('#add_cart').click(function () {
        $(".cart_mask").css("display", "block");
        $(".small_cart").css("display", "block");
    });

    $(".close_icon").click(function () {
        $(".small_cart").css("display", "none");
        $(".cart_mask").css("display", "none");
    });
    $(".continue").click(function () {
        $(".small_cart").css("display", "none");
        $(".cart_mask").css("display", "none");
    });
    $(".cart_mask").click(function () {
        $(".small_cart").css("display", "none");
        $(".cart_mask").css("display", "none");
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var openPhotoSwipe = function () {
        var pswpElement = document.querySelectorAll('.pswp')[0];
        var items = [];

        // Function to load an image and return a promise
        function loadImage(src) {
            return new Promise((resolve, reject) => {
                var img = new Image();
                img.src = src;
                img.onload = function () {
                    resolve({
                        src: img.src,
                        w: img.naturalWidth,
                        h: img.naturalHeight
                    });
                };
                img.onerror = reject;
            });
        }

        // Load all images and initialize PhotoSwipe
        Promise.all(imageUrls.map(loadImage))
            .then((loadedItems) => {
                items = loadedItems;
                var options = {
                    index: 0
                };
                var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
                gallery.init();
            })
            .catch((error) => {
                console.error('Error loading images:', error);
            });
    };
    document.querySelector('.swiper-wrapper').addEventListener('click', openPhotoSwipe);
});