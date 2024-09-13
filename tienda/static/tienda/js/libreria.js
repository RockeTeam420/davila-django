<<<<<<< HEAD

function eliminar(url) {
    if (confirm("Está seguro?")) {
=======
console.log("Hola mundo...!")
//alert("Hola mundo!!")

function eliminar(url){
    if(confirm("Está seguro?")){
>>>>>>> origin/main
        location.href = url;
    }
}

<<<<<<< HEAD
function add_carrito(url, id_producto) {
=======
function add_carrito(url, id_producto){
>>>>>>> origin/main
    csrf_token = $("[name='csrfmiddlewaretoken']")[0].value;
    id = $(`#id_${id_producto}`).val()
    cantidad = $(`#cantidad_${id_producto}`).val()
    items_carrito = $("#items_carrito")

    // Capturo referencia a dom de carrito del offCanvas
    contenido = $("#respuesta_carrito")
    loader = $("#loader")

    loader.removeClass("d-none");
    loader.addClass("d-block");

    offCanvas_carrito = $("#offcanvasRight");
    offCanvas_carrito.offcanvas('toggle');

    $.ajax({
        url: url,
        type: "POST",
<<<<<<< HEAD
        data: { "csrfmiddlewaretoken": csrf_token, "id": id, "cantidad": cantidad }
    })
        .done(function (respuesta) {

            if (respuesta != "Error") {

                loader.removeClass("d-block");
                loader.addClass("d-none");
                // Pintar respuesta en offCanvas
                contenido.html(respuesta);

                //Buscar items en html resultante
                let position_ini = respuesta.search(" ");
                let position_final = respuesta.search("</h1>");
                let result = respuesta.substring(position_ini + 2, position_final - 1);
                items_carrito.html(result);
            }
            else {
                location.href = "/tienda/inicio/";
            }
        })
        .fail(function (respuesta) {
            location.href = "/tienda/inicio/";
        });
}


function ver_carrito(url) {
=======
        data: {"csrfmiddlewaretoken": csrf_token, "id": id, "cantidad": cantidad}
    })
    .done(function(respuesta){

        if (respuesta != "Error"){

            loader.removeClass("d-block");
            loader.addClass("d-none");
            // Pintar respuesta en offCanvas
            contenido.html(respuesta);

            //Buscar items en html resultante
            let position_ini = respuesta.search(" ");
            let position_final = respuesta.search("</h1>");
            let result = respuesta.substring(position_ini+2, position_final-1);
            items_carrito.html(result);
        }
        else{
            location.href="/tienda/inicio/";
        }
    })
    .fail(function(respuesta){
        location.href="/tienda/inicio/";
    });
}


function ver_carrito(url){
>>>>>>> origin/main
    // Capturo referencia a dom de carrito del offCanvas
    contenido = $("#respuesta_carrito")
    loader = $("#loader")

    loader.removeClass("d-none");
    loader.addClass("d-block");

    offCanvas_carrito = $("#offcanvasRight");
    offCanvas_carrito.offcanvas('toggle');

    $.ajax({
        url: url
    })
<<<<<<< HEAD
        .done(function (respuesta) {

            if (respuesta != "Error") {
                /*setTimeout(()=>{
                    loader.removeClass("d-block");
                    loader.addClass("d-none");
                    // Pintar respuesta en offCanvas
                    contenido.html(respuesta);
                }, 3000);*/

=======
    .done(function(respuesta){

        if (respuesta != "Error"){
            /*setTimeout(()=>{
>>>>>>> origin/main
                loader.removeClass("d-block");
                loader.addClass("d-none");
                // Pintar respuesta en offCanvas
                contenido.html(respuesta);
<<<<<<< HEAD

            }
            else {
                location.href = "/tienda/inicio/";
            }
        })
        .fail(function (respuesta) {
            location.href = "/tienda/inicio/";
        });
}

function eliminar_item_carrito(url) {
=======
            }, 3000);*/

            loader.removeClass("d-block");
            loader.addClass("d-none");
            // Pintar respuesta en offCanvas
            contenido.html(respuesta);

        }
        else{
            location.href="/tienda/inicio/";
        }
    })
    .fail(function(respuesta){
        location.href="/tienda/inicio/";
    });
}

function eliminar_item_carrito(url){
>>>>>>> origin/main
    contenido = $("#respuesta_carrito")
    items_carrito = $("#items_carrito")
    loader = $("#loader")

    loader.removeClass("d-none");
    loader.addClass("d-block");

    $.ajax({
        url: url
    })
<<<<<<< HEAD
        .done(function (respuesta) {

            if (respuesta != "Error") {

                loader.removeClass("d-block");
                loader.addClass("d-none");
                // Pintar respuesta en offCanvas
                contenido.html(respuesta);

                //Buscar items en html resultante
                let position_ini = respuesta.search(" ");
                let position_final = respuesta.search("</h1>");
                let result = respuesta.substring(position_ini + 2, position_final - 1);
                items_carrito.html(result);
            }
            else {
                location.href = "/tienda/";
            }
        })
        .fail(function (respuesta) {
            location.href = "/tienda/";
        });
}

function actualizar_totales_carrito(url, id) {
    contenido = $("#respuesta_carrito")
    loader = $("#loader")
    cantidad = $("#cantidad_carrito_" + id)
=======
    .done(function(respuesta){

        if (respuesta != "Error"){

            loader.removeClass("d-block");
            loader.addClass("d-none");
            // Pintar respuesta en offCanvas
            contenido.html(respuesta);

            //Buscar items en html resultante
            let position_ini = respuesta.search(" ");
            let position_final = respuesta.search("</h1>");
            let result = respuesta.substring(position_ini+2, position_final-1);
            items_carrito.html(result);
        }
        else{
            location.href="/tienda/inicio/";
        }
    })
    .fail(function(respuesta){
        location.href="/tienda/inicio/";
    });
}

function actualizar_totales_carrito(url, id){
    contenido = $("#respuesta_carrito")
    loader = $("#loader")
    cantidad = $("#cantidad_carrito_"+id)
>>>>>>> origin/main

    loader.removeClass("d-none");
    loader.addClass("d-block");

    $.ajax({
        url: url,
        type: "GET",
<<<<<<< HEAD
        data: { "cantidad": cantidad.val() }
    })
        .done(function (respuesta) {

            if (respuesta != "Error") {

                loader.removeClass("d-block");
                loader.addClass("d-none");
                // Pintar respuesta en offCanvas
                contenido.html(respuesta);
            }
            else {
                location.href = "/tienda/inicio/";
            }
        })
        .fail(function (respuesta) {
            location.href = "/tienda/inicio/";
        });
=======
        data: {"cantidad": cantidad.val()}
    })
    .done(function(respuesta){

        if (respuesta != "Error"){

            loader.removeClass("d-block");
            loader.addClass("d-none");
            // Pintar respuesta en offCanvas
            contenido.html(respuesta);
        }
        else{
            location.href="/tienda/inicio/";
        }
    })
    .fail(function(respuesta){
        location.href="/tienda/inicio/";
    });
>>>>>>> origin/main
}