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
        let price = parseFloat($('#gprice').attr('data-price'));
        console.log("price: ", price); // Log the value of total
        let total = num * price;
        console.log("Total value: ", total); // Log the value of total
        $('.num_show').val(num);
        $('#gtotal').text(total.toLocaleString('de-DE') + '₫');
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

document.addEventListener("DOMContentLoaded", function() {
    var priceElements = document.querySelectorAll('.prize');
    priceElements.forEach(function(element) {
        var price = parseFloat(element.getAttribute('data-price'));
        element.textContent = price.toLocaleString('de-DE') + '₫';
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var elements = ['gprice', 'gtotal'];
    elements.forEach(function(id) {
        var element = document.getElementById(id);
        if (element) {
            var price = parseFloat(element.getAttribute('data-price'));
            element.textContent = price.toLocaleString('de-DE') + '₫';
        }
    });
});
