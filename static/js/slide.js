$(function () {
    var $slides = $(".slide_pics li"),
        len = $slides.length,
        nowli = 0,
        prevli = 0,
        ismove = false,
        timer = null;

    var $prev = $(".prev"),
        $next = $(".next"),
        $pointsContainer = $(".points");

    // Initialize: Position all slides except the first
    $slides.not(":first").css({ left: 760 });

    // Generate points for slider navigation
    for (var i = 0; i < len; i++) {
        $("<li>").toggleClass("active", i === 0).appendTo($pointsContainer);
    }

    var $points = $(".points li");

    // Auto-play the slider every 4 seconds
    function startAutoplay() {
        timer = setInterval(nextSlide, 4000);
    }

    function stopAutoplay() {
        clearInterval(timer);
    }

    startAutoplay();

    $(".slide").hover(stopAutoplay, startAutoplay);

    // Next Slide
    function nextSlide() {
        if (ismove) return;
        nowli = (nowli + 1) % len;
        moveSlide();
    }

    // Previous Slide
    function prevSlide() {
        if (ismove) return;
        nowli = (nowli - 1 + len) % len;
        moveSlide();
    }

    function moveSlide() {
        if (nowli === prevli) return;

        ismove = true;
        var direction = nowli > prevli ? 760 : -760;

        $slides.eq(nowli).css({ left: direction * (nowli > prevli ? 1 : -1) });

        $slides.eq(prevli).animate({ left: -direction }, 800, "swing");
        $slides.eq(nowli).animate({ left: 0 }, 800, "swing", function () {
            ismove = false;
        });

        $points.eq(nowli).addClass("active").siblings().removeClass("active");
        prevli = nowli;
    }

    $next.click(nextSlide);
    $prev.click(prevSlide);

    $points.click(function () {
        if (ismove) return;
        nowli = $(this).index();
        moveSlide();
    });
});
