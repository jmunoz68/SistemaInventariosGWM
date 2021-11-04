
function fijar_saltoModal(document, claseMod, ruta, campoId='',
                              modalClassBody, modalIdSeccion) {
    $(document).ready(function(){
        $(claseMod).click(function(){
            var id = $(this).data(campoId);
            $.ajax({
                url: ruta,
                type: 'post',
                data: {'id': id},
                success: function(data){ 
                    $(modalClassBody).html(data); 
                    $(modalClassBody).append(data.htmlresponse);
                    $(modalIdSeccion).modal('show'); 
                }
            });
        });
    });
}


function fijar_saltoModal_index(document, claseMod, rutaEval, 
                              modalClassBody, modalIdSeccion) {
    $(document).ready(function(){
        $(claseMod).click(function(){
            // alert("entro1");
            // Esto se ejecuta cuando se hace click en la "claseMod".
            var usr = document.getElementById('username').value;
            var pss = document.getElementById('password').value;
            // Ejecuta el ajax.
            $.ajax({
                // En el ajax hace un llamado a la "rutaEval" de forma "post", pasando como parametros la "data".
                url: rutaEval,
                type: 'post',
                data: {'username': usr, 'password': pss},
                // El success ocurre cuando la "rutaIni" retorna la "rtaData" desde Python con "jsonify()"
                success: function(rtaData){ 
                    // alert("entro2");
                    //console.log("rtaData:", rtaData);
                    //console.log("rta:", rtaData.rta);
                    //console.log("otraRuta:", rtaData.otraRuta);
                    //console.log("rtaData.htmlresponse:", rtaData.htmlresponse);
                    if (rtaData.rta == 1) {
                        // Se muestra la ventana modal.
                        //console.log("entro 1");
                        $(modalClassBody).html(rtaData); 
                        $(modalClassBody).append(rtaData.htmlresponse);
                        $(modalIdSeccion).modal('show'); 
                    } else if (rtaData.rta == 2){
                        //console.log("entro 2");
                        // Se abre "otraRuta" en la misma ventana.
                        window.open(rtaData.otraRuta, "_self");
                    }
                }
            });
        });
    });
}


function fijar_abrirNuevoTab(document, idSeccion, url) {
    $(document).ready(function(){
        $(idSeccion).click(function(){
            // Abrir nuevo tab
            var win = window.open(url, '_blank');
            // Cambiar el foco al nuevo tab (punto opcional)
            win.focus();
        });
    });
}


