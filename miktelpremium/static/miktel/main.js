// /**
//  * Created by Jacek on 2016-01-12.
//  */
// // document.addEventListener('DOMContentLoaded', function () {
// var active_forms = document.querySelectorAll('div.show');
// var zakup = document.querySelectorAll('#zakup');

// var select = document.querySelector('#rodzaj');

// // $(document).ready(function () {
// //     $("div.show").click(function () {
// //         $("div").hide();
// //     });
// // });


// //Wyłącz wszystkei img
// active_forms.forEach((el) => {
//     el.style.display = 'None'
// });

// //Włącz pierwszy img dla option domyślnej
// active_forms[0].style.display = 'block'

// //zmiana img dla option selected
// select.addEventListener("change", function () {
//     var currentOpt = select.options[select.selectedIndex];
//     value = currentOpt.innerHTML

//     if (value == 'Telefon zakup') {
//         zakup.style.display = 'block'
//     } else {
//         zakup.style.display = 'none'
//     };
// });
// $("#usluga").show();
// $("#sprzedaz").hide();
// $("#zakup").hide();

// $(function () {
//     $("#rodzaj").change(function () {
//         var val = $(this).val();
//         if (val == 7) {
//             $("#zakup").show();
//             $("#usluga").hide();
//             $("#sprzedaz").hide();
//         } else if (val == 9) {
//             $("#sprzedaz").show();
//             $("#zakup").hide();
//             $("#usluga").hide();
//         } else {
//             $("#usluga").show();
//             $("#sprzedaz").hide();
//             $("#zakup").hide();
//         }
//     });
// });

// });

$(document).ready(function () {
    $('#search').keyup(function () {
        //pole szukaj
        var text = $(this).val();

        //na dziendobry ukryj wszystko po nacisnieciu klawisza
        $('.lista').hide();

        //lecz nastepnie pokaż pasujące frary
        $('.lista:contains("' + text + '")').show();

    });
});

$(document).ready(function () {
    $('#search2').change(function () {
        //pole szukaj
        var text = $(this).val();

        //na dziendobry ukryj wszystko po nacisnieciu klawisza
        $('.lista').hide();

        //lecz nastepnie pokaż pasujące frary
        $('.lista:contains("' + text + '")').show();

    });
});




$(document).ready(function () {

    var wybierz = $('#wybierz').css({
        "color": "red"
    });
    var button = $('#ready_button').hide();

    $('#wybierz_serwis').change(function () {

        if ($(this).val() != "") {
            wybierz.html("OK").css({
                "color": "green"
            });
            button.show();

        } else {
            wybierz.html("Nie wybrano").css({
                "color": "red"
            });
            button.hide();
        };
    });
});


// $(document).ready(function () {

//     var ilosc = $('#ilosc').css({
//         "color": "red"
//     });
//     var plus = $('#plus');
//     var minus = $('#minus');
//     var i = 0;

//     plus.click(function () {
//         ilosc.val(i);
//         i++;
//     });
//     minus.click(function () {
//         ilosc.val(i);
//         i--;

//     });
// });