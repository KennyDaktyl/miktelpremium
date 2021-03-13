$(document).ready(function () {

    var pay_rate = $('#pay_rate').data('pay_rate');
    pay_rate = parseFloat(pay_rate);

    var hours_count = $('#id_hours_count').val();
    hours_count = parseFloat(hours_count)
    var input = $('#id_value')
    input.val(pay_rate);

    $("#id_hours_count").on("change", function () {
        input.val(pay_rate * $(this).val());
    });



});