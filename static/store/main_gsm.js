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
                    //url: "http://127.0.0.1:8000/api-view/phones/",
                    url: "https://www.miktel.krakow.pl/api-view/phones/",
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
                                var id = result[i]['id'];
                                var slug = result[i].slug;
                                var marka = result[i].marka['nazwa'];
                                var name = result[i].nazwa;
                                name = name.replace(' ', "_");
                                var typ = result[i].kategoria['nazwa'];
                                var price = result[i].cena_sprzed;
                                // var count = result[i].ilosc;
                                var shop = result[i].magazyn_aktualny['nazwa_slug'];
                                var shop_adrress = result[i].magazyn_aktualny['nazwa_slug'] + "-" + result[i].magazyn_aktualny.adres['miasto_slug'] + "-" + result[i].magazyn_aktualny.adres['ulica_slug'];;
                                var new_a = $('<a/>', {

                                    text: marka + " " + name + ", typ: " + typ + ", cena: " + price + "zł" + ", dostepny: " + shop,
                                    class: 'col-12 mx-auto p-0 mb-2 mt-2 ml-0 mr-0 text-dark bg-white',
                                    href: "/produkt/telefony-komorkowe-dostepne-w-sklepach-miktel/" + slug + "/" +
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
