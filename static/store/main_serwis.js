$(document).ready(function () {
    var input = $('#input');
    var link = $('#link');
    link.css('display', 'none');
    var div_link = $('#div_link');
    div_link.css('display', 'none');
    var table_products = $('#table_products');
    var url_adress = window.location.href;
    var new_line = $('<br>');


    input.keyup(function (event) {

        if ($(this).val().length > 1) {
            var search = $(this).val();

            function GetSearchResult() {
                result = "";
                $.ajax({
                    //url: "http://127.0.0.1:8000/api-view/items/",
                    url: "https://www.miktel.krakow.pl/api-view/items/",
                    // url: url_adress,
                    async: true,
                    type: "GET",
                    // type: "POST",
                    data: {
                        search: search,
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    dataType: "json",
                    success: function (data) {
                        result = JSON.parse(JSON.stringify(data));
                        console.log(result);
                        link.text('');
                        if (result.length > 0) {
                            link.css('display', 'grid');
                            div_link.css('display', 'grid');
                            for (var i = 0; i < result.length; i++) {
                                console.log(result[i]['id']);
                                var id = result[i]['id'];
                                var slug = result[i].slug;
                                var marka = result[i].marka['nazwa'];
                                var name = result[i]['nazwa'];
                                name = name.replace(' ', "-");
                                var typ = result[i].typ['nazwa'];
                                typ = typ.replace(' ', "-");
                                typ = typ.replace('ś', "s");
                                var price = result[i].cena_sprzed;
                                var count = result[i].ilosc;
                                var new_a = $('<a/>', {
                                    text: marka + " " + name + ", typ: " + typ + ", cena: " + price + "zł" + ", szt.: " + count,
                                    class: 'col-12 mx-auto p-0 mb-2 mt-2 ml-0 mr-0 text-dark bg-white',
                                    href: "/produkt/serwis-telefonow-komorkowych-oferta-cennik/" + slug + "/" +
                                        id,

                                })
                                new_a.appendTo(link);
                                // return result;
                            }
                        } else {
                            link.text('');
                            link.css('display', 'none');
                            div_link.css('display', 'none');
                        }
                    }
                });
                return result;
            }

            result = GetSearchResult();
        } else {
            link.text('');
            link.css('display', 'none');
            div_link.css('display', 'none');
        }
    });



})
