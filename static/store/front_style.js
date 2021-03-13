$(document).ready(function () {
    var links = $('div.hidden');
    var nav = $('nav.navbar');
    // var captcha = $('p:nth-child(1) > label');
    // captcha.css('display', 'none');
    // // var div_captcha = $('div.g-recaptcha div');
    // var div_captcha = $('#id_captcha div');
    // div_captcha.addClass("mx-auto");
    $(window).on('wheel', function (event) {
        if (event.originalEvent.deltaY < 0) {
            links.removeClass('scroll_down');
            nav.removeClass('active');
        } else {
            links.addClass('scroll_down');
            nav.addClass('active');
        }
    });

    var lastY;
    $(window).bind('touchmove', function (e) {
        var currentY = e.originalEvent.touches[0].clientY;
        if (currentY > lastY) {
            links.removeClass('scroll_down');
            nav.removeClass('active');
        } else if (currentY < lastY) {
            links.addClass('scroll_down');
            nav.addClass('active');
        }
        lastY = currentY;
    });
})