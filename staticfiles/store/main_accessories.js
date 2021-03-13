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
                    url: "http://127.0.0.1:8000/api-view/products",
                    // url: "https://www.miktel.krakow.pl/api-view/products",
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
                                var prod_name = (result[i]['name']);
                                var slug = (result[i]['slug']);
                                var id = result[i]['id'];
                                var cat_name = (result[i]['category_id']['name'])
                                var slug_ctg = (result[i]['category_id']['slug'])
                                var slug_prf = (result[i]['category_id']['profile_id']['slug'])
                                var price = result[i]['price'];
                                var new_a = $('<a/>', {
                                    text: cat_name + " " + prod_name + ", cena: " + price + "zł",
                                    class: 'col-12 mx-auto p-0 mb-2 mt-2 ml-0 mr-0 text-dark bg-white',
                                    href: "/produkty/" + slug_prf + "/" + slug_ctg + "/" + slug + "/" +
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