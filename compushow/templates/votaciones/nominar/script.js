/**@class
 * Clase Categoria
 * @description
 * clase contenedora de representacion de Categoria.
 * @author Oliver Perez
 */
var Categoria = Class.create({
    /**
     * @constructor
     * @param $super ignorar.
     * @param {Compra} compra Referencia a el objeto compra relacionado.
     */
    initialize : function(/**Strin*/ nombre, /**Strin*/ descripcion,
        /**Int*/ maximo, /**Int*/ minimo, /**Boolean*/ computistas) {
        
        this.nombre      = nombre;
        this.descripcion = descripcion;
        this.maximo      = maximo;
        this.minimo      = minimo;
        this.computistas = computistas;
    }
});

function categoria_actual() {
    var categoria_elm = $("categoria"),
    option = categoria_elm.options[categoria_elm.selectedIndex];
    return categorias[option.value];
}

function actualizar_boton_agregar_nominado() {
    var categoria = categoria_actual();

    if(categoria.maximo > nominados) {
        $("boton_agregar_nominado").show();
    } else {
        $("boton_agregar_nominado").hide();
    }
}

function cambio_de_categoria() {
    var categoria = categoria_actual();

    $("descripcion_categoria").update(categoria.descripcion);

    while(nominados > categoria.maximo) borrar_nominado();
    while(nominados < categoria.minimo) agregar_nominado();
    actualizar_boton_agregar_nominado();
}

function agregar_nominado() {
    var categoria = categoria_actual();
    
    if(categoria.maximo > nominados) {
        var id             = "nominado"+nominados,

        table          = new Element("TABLE",{"style":"width:100%"}),
        fila           = new Element("TR"),
        col1           = new Element("TD"),
        col2           = new Element("TD"),
        input          = new Element("INPUT", {
            "spellcheck":"false",
            "name":id,
            "id":"input_"+id,
            "onkeyup":"consultar_nombre("+nominados+")"
        }),
        autoComp       = new Element("LABEL", {
            "id":"complNominado"+nominados,
            "class":"autoCompletado"
        }),
        nuevo_nominado = new Element("LABEL"),
        nuevo_nominado2 = new Element("LABEL"),
        nominado_cont  = new Element("DIV"  , {
            "id":id,
            "class":"nominado"
        });
                            
        /*nuevo_nominado
        .insert(new Element("STRONG").update("Nominar a:"))
        .insert(autoComp)
        .insert(input);

        nominado_cont.insert(nuevo_nominado);*/
        
        //nuevo_nominado.insert(new Element("DIV", {'class' : "divBorrar", "onclick":"borrar_nominado_n("+nominados+")"}));

        col1.insert(nuevo_nominado.insert(input));
        col2.insert(nuevo_nominado2.insert(new Element("STRONG").update("Nominar a:")).insert(autoComp));
        table.insert(fila.insert(col1).insert(col2));

        nominado_cont.insert(table);

        $("lista_nominados").insert(nominado_cont);
        
        nominados++;
    }

    actualizar_boton_agregar_nominado();
}

function borrar_nominado() {
    var categoria = categoria_actual();

    if(categoria.minimo < nominados) {
        $("nominado"+(--nominados)).remove();
    }
}

function consultar_nombre(numero) {
    var categoria = categoria_actual(),
    elm_nombre = "complNominado"+numero;

    if(categoria.computistas) {
        new Ajax.Updater(elm_nombre, "/consultar_nombre", {
            method: 'get',
            parameters: {
                "busqueda":$("input_nominado"+numero).value
            }
        });
    } else {
        $(elm_nombre).value = $("input_nominado"+numero).value;
    }
}

function actualizar_boton_eliminar_foto() {
    if(fotos>0) $("boton_eliminar_foto").show();
    else $("boton_eliminar_foto").hide();
}

function validar_foto(campo) {
    var foto_regexp = new RegExp(/\.(jpg|gif|jpeg|png)$/);
    var valido = foto_regexp.test(campo.value);
    if (valido){
        return true;
    }
    else {
        alert("Solo puedes subir fotos");
        return false;
    }
}

function habilitarNominarFoto(){
    var nombreFoto = validar_foto($("input_foto0"));
    if (nombreFoto) $("iniciar_btn").disabled = false;
    else $("iniciar_btn").disabled = true;
}

function agregar_foto() {
    var id            = "foto"+fotos,
        input         = new Element("INPUT", {"name":id, "id":"input_"+id, "type":"file", "accept":"image/*"}),
        foto_cont     = new Element("DIV"  , {"id":id, "class":"cont_input_media"});

    foto_cont.insert(input);
    
    $("lista_fotos").insert(foto_cont);
    
    fotos++;

    actualizar_boton_eliminar_foto();
    //validateForm();
}

function eliminar_foto() {
    if(fotos > 0) {
        $("foto"+(--fotos)).remove();
        actualizar_boton_eliminar_foto();
    }
}



function actualizar_boton_eliminar_video() {
    if(videos>0) $("boton_eliminar_video").show();
    else $("boton_eliminar_video").hide();
}

function agregar_video() {
    var id            = "video"+videos,
        input         = new Element("INPUT", {"name":id, "id":"input_"+id, "class":"prev_img", "size":"32","onkeyup":"actualizar_video_prev("+videos+");"}),
        preview       = new Element("IMG"  , {"id":"prev_"+id, "class":"prev_img","height":"20px" ,"src":"/templates/votaciones/media/Error.png"}),
        video_cont    = new Element("DIV"  , {"id":id, "class":"cont_input_media"});

    video_cont.insert(preview).insert(input);

    $("lista_videos").insert(video_cont);

    videos++;

    actualizar_boton_eliminar_video();
}

function eliminar_video() {
    if(videos > 0) {
        $("video"+(--videos)).remove();
        actualizar_boton_eliminar_video();
    }
}

function extraer_video_id(video_num) {
    if(videos > video_num){
        var video_link        = $("input_video"+video_num).value,
            video_id          = video_link.split('v=')[1];

        if(video_id == null) return null;
        
        var ampersandPosition = video_id.indexOf('&');

        if(ampersandPosition != -1) {
            video_id = video_id.substring(0, ampersandPosition);
        }
        return video_id;
    }
    return null;
}

function actualizar_video_prev(video_num) {
    var video_id = extraer_video_id(video_num),
        video_prev = $("prev_video"+video_num);

    if(video_id != null) {
        video_prev.setAttribute("src", "http://img.youtube.com/vi/"+video_id+"/2.jpg");
        video_prev.setAttribute("height", "80px");
    } else {
        video_prev.setAttribute("src", "/templates/votaciones/media/Error.png");
        video_prev.setAttribute("height", "20px");
    }
}


function nominar() {
    var i, video_id, foto_id, input,
        form      = $("form_nominar"),
        categoria = categoria_actual();


    for(i = 0; i < nominados; i++) {
        input = $("input_nominado"+i);
        if(categoria.computistas) {
            input.value = $("complNominado"+i).innerHTML;
        }
        if(input.value==null || input.value.trim() == "") {
            alert("El campo "+(i+1)+"° de los nominados es invalido.");
            return false;
        }
    }

    
    for(i = 0; i < fotos; i++) {
        foto_id = "input_foto" + i;
        if($(foto_id).value==null || $(foto_id).value=="") {
            alert("El campo "+(i+1)+"° de las fotos esta vacio.");
            return false;
        }
    }
    

    for(i = 0; i < videos; i++) {
        video_id = extraer_video_id(i);
        if(video_id != null) {
            $("input_video"+i).value = video_id;
        } else {
            alert("El campo "+(i+1)+"° de link a youtube es invalido.")
            return false;
        }
    }

    form.insert(new Element("INPUT", {
        "type":"hidden",
        "name":"nominados",
        "value":nominados
    })).insert(new Element("INPUT", {
        "type":"hidden",
        "name":"videos",
        "value":videos
    }));

    return true;
}

/*
function borrar_nominado_n(numero) {
    categoria = categoria_actual();

    if(categoria.minimo < nominados) {
        $("nominado"+numero).remove();
        nominados--;
    }
}
*/

function eliminar_voto(voto_id){
    if(confirm("¿Desea borrar esta nominacion?")) {
        new Ajax.Request('/borrar_voto_nominacion',
        {
            method:'post',
            parameters: {
                "id":voto_id
            },
            onSuccess: function(transport){
                if(transport.responseText === '1') {
                    $("nominacion"+voto_id).remove();
                } else {
                    alert("Ocurrio un error en el servidor =s");
                }
                
            },
            onFailure: function(){
                alert('No se pudo eliminar la nominacion\nintente más tarde.')
            }
        });
    }
}
