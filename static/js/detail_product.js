$(document).ready(function () {
    // Initialize show_count from local storage
    let storedCount = localStorage.getItem('show_count');
    if (storedCount != 'undefined') {
        $('#show_count').text(storedCount);
    }
    else { $('#show_count').text('0'); }

    $(".buy_btn").on("click", function () {
        let num = parseInt($('.num_show').val(), 10);
        let productId = $(this).data('product-id');

        $.get(`/cart/add${productId}_${num}/`, function (data) {
            $('#show_count').text(data.count);
            localStorage.setItem('show_count', data.count);
            location.href = "/cart/";
        }).fail(function () {
            alert('Error adding to cart. Please try again.');
        });
    });

    $(".add_cart").on("click", function () {
        let productId = $(this).data('product-id');
        let num = parseInt($('.num_show').val(), 10);
        
        let $addBtn = $(this);
        let $showCount = $('#show_count');
        let $add_x = $addBtn.offset().top;
        let $add_y = $addBtn.offset().left;
        let $to_x = $showCount.offset().top;
        let $to_y = $showCount.offset().left;

        $(".add_jump").css({ 'left': $add_y + 80, 'top': $add_x + 10, 'display': 'block' });

        // Check if the user is logged in
        if ($('.login_btn').text().includes('Login')) {
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
                let count = parseInt($('.num_show').val(), 10);
                $showCount.text(count);
            });
        });

        $.get(`/cart/add${productId}_${num}/`, function (data) {
            $showCount.text(data.count);
            localStorage.setItem('show_count', data.count);
        }).fail(function () {
            alert('Error adding to cart. Please try again.');
        });
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


function plus() {
    let num = parseFloat($('.num_show').val());
    $('.num_show').val(num + 1);
    $('.num_show').blur();
}

function minus() {
    let num = parseFloat($('.num_show').val());
    if (num > 1) {
        $('.num_show').val(num - 1);
        $('.num_show').blur();
    }
}

$(function () {
    $('.num_show').blur(function () {
        let num = parseInt($('.num_show').val());
        if (num < 1) num = 1;
        $('.num_show').val(num);
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const swiper = new Swiper('.swiper-container', {
        loop: true,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
    });
});
