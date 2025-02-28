$(document).ready(function () {
    $(".buy_btn").click(function () {
        let num = parseInt($('.num_show').val());
        $.get('/cart/add{{ productId }}_' + num + '/', function (data) {
            $('#show_count').text(data.count);
        });
        location.href = "/cart/";
    });

    $('#add_cart').click(function () {
        let $add_x = $('#add_cart').offset().top;
        let $add_y = $('#add_cart').offset().left;
        let $to_x = $('#show_count').offset().top;
        let $to_y = $('#show_count').offset().left;

        $(".add_jump").css({ 'left': $add_y + 80, 'top': $add_x + 10, 'display': 'block' });

        // Check login or not
        if ($('.login_btn').text().indexOf('Login') >= 0) {
            alert('Please login first');
            location.href = '/user/login/';
            return;
        }

        // Add to cart animation
        $(".add_jump").stop().animate({
            'left': $to_y + 7,
            'top': $to_x + 7
        }, "fast", function () {
            $(".add_jump").fadeOut('fast', function () {
                let count = $('.num_show').val();
                // $('#show_count').html(count);
            });
        });

        let num = parseInt($('.num_show').val());
        $.get('/cart/add' + productId + '_' + num + '/', function (data) {
            $('#show_count').text(data.count);
        }).fail(function () {
            alert('Error adding to cart. Please try again.');
        });

        // Update the num_show value
        let currentVal = parseInt($('.show_count').val());
        $('.show_count').val(currentVal + 1);
    });

    $('#add_cart').click(function () {
        $(".cart_mask").css("display", "block");
        $(".small_cart").css("display", "block");
    });


    $(".close_icon, .continue, .cart_mask").click(function () {
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