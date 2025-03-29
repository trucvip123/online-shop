$(document).ready(function () {
    $(".buy_btn").on("click", function () {
        let num = parseInt($('.num_show').val(), 10);
        let productId = $(this).data('product-id');

        $.get(`/cart/add${productId}_${num}/`, function (data) {
            $('#show_count').text(data.count);
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
            });
        });

        $.get(`/cart/add${productId}_${num}/`, function (data) {
            $showCount.text(data.count);
        }).fail(function () {
            alert('Error adding to cart. Please try again.');
        });
    });

    // Handle YouTube video modal
    $('.swiper-container').on('click', '.swiper-slide[data-video-url]', function (e) {
        e.stopPropagation(); // Prevent triggering other click events
        const videoUrl = $(this).data('video-url') + '?autoplay=1';
        $('#videoIframe').attr('src', videoUrl);
        $('#videoModal').modal('show');
    });

    // Clear the iframe when the modal is closed
    $('#videoModal').on('hidden.bs.modal', function () {
        $('#videoIframe').attr('src', '');
    });

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

    // Open PhotoSwipe for image slides only
    const pswpElement = document.querySelectorAll('.pswp')[0];
    const items = [];
    document.querySelectorAll('.swiper-slide[data-type="image"]').forEach((slide) => {
        items.push({
            src: slide.getAttribute('data-src'),
            w: 1200, // Default width
            h: 800, // Default height
        });
    });

    const openPhotoSwipe = function (index) {
        const options = {
            index: index,
            addCaptionHTMLFn: function (item, captionEl) {
                captionEl.children[0].innerHTML = item.title || '';
                return true;
            },
        };
        const gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
        gallery.init();
    };

    // Add click event to image slides only
    document.querySelectorAll('.swiper-slide[data-type="image"]').forEach((slide, index) => {
        slide.addEventListener('click', () => {
            openPhotoSwipe(index);
        });
    });
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
