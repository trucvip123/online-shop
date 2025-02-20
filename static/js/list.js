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
