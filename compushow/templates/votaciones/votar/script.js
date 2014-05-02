/**@class
 * Clase Categoria
 * @description
 * clase contenedora de representacion de Categoria.
 * @author Oliver Perez
 */
var Categoria = Class.create({
    /**
     * @constructor
     * @param {nombre} .
     * @param {descripcion} .
     *
     */
    initialize : function(/**String*/ nombre, /**String*/ descripcion) {
        this.nombre       = nombre;
        this.descripcion  = descripcion;
        this.nominaciones = [];
    }
});

/**@class
 * Clase Nominacion
 * @description
 * clase contenedora de representacion de una Nominacion.
 * @author Oliver Perez
 */
var Nominacion = Class.create({
    /**
     * @constructor
     * @param {nominados} .
     * @param {foto_id} .
     * @param {media} .
     */
    initialize : function(id, nominados, foto_id) {
        this.id        = id;
        this.nominados = nominados;
        this.foto_id   = foto_id;
        this.media     = [];
        this.votado    = false;
    },
    toString: function() {
        var votado_class = this.votado ? "votado" : "no_votado";
        var str = "<div id='nominado"+this.id+"' class='nominado "+votado_class+"' onclick='cambiar_nominado("+this.id+")'></td>";
        str += "<table><tr><td><div class='imagen'><img src='"+this.foto_id+"' height='64' ></div></td>";
        str += "<td><div class='nombres'>";
        str += this.nominados.join("<br>");
        str += "</td></tr></table></div></div>";
        return str;
    }
});

/**@class
 * Clase Media
 * @description
 * clase contenedora de representacion de una Foto o un Video).
 * @author Oliver Perez
 */
var Media = Class.create({
    /**
     * @constructor
     * @param {nominados} .
     * @param {foto_id} .
     * @param {media} .
     */
    initialize : function(id, url, esVideo) {
        this.id      = id;
        this.url     = url;
        this.esVideo = esVideo;
    },
    toString: function() {
        if(this.esVideo) {
            return "http://img.youtube.com/vi/"+this.url+"/2.jpg";
        } else {
            return this.url;
        }
    }
});

function categoria_actual() {
    return categorias[categoria_ind];
}

function cambiar_categoria(id) {
    var categoria = categoria_actual();

    if(categoria != null) $("categoria"+categoria_ind).removeClassName('seleccionado')

    $("categoria"+id).addClassName('seleccionado');

    categoria_ind = id;
    
    llenar_lista_nominados();
}

function llenar_lista_nominados() {
    var categoria = categoria_actual();

    $("cont_votacion").update("<h1 id='titulo_categoria'></h1><div id='lista_nominados'></div><div id='detalles_nominado'></div>");

    $("titulo_categoria").update(categoria.nombre);
    $("lista_nominados").update(categoria.nominaciones.join('\n'));
    
    $("detalles_nominado").update(DIV_ayuda("Selecciona a un nominado para sus fotos y así poder votar por él."));
    $("detalles_nominado").insert(DIV_ayuda(categoria.nombre+": <p>"+categoria.descripcion+".</p>"));
}

function cambiar_nominado(id) {
    var contenido = new Element("DIV", {"id":"renglon_superior"}),
        nominados = new Element("DIV", {"id":"nominados"});
    
    for(var i=0; i< nominaciones[id].nominados.length; i++) {
        nominados.insert(new Element("DIV").update(nominaciones[id].nominados[i]));
    }
    
    contenido.insert(nominados);
    if(nominaciones[id].votado) {
        contenido.insert(new Element("DIV", {"id":"boton_votar", "class":"votar_no", "onclick":"votar("+id+")"}).update("Quitar Voto"));
    } else {
        contenido.insert(new Element("DIV", {"id":"boton_votar", "class":"votar_si", "onclick":"votar("+id+")"}).update("Votar"));
    }
    
    
    $("detalles_nominado").update(contenido);

    var media     = nominaciones[id].media,
        media_len = media.length,
        ayuda     = "";

    if(media_len > 0) ayuda = "Selecciona alguna foto en la lista de abajo para verla más grande.";
    
    $("detalles_nominado").insert(new Element("DIV", {"id":"vista_media"}).update(DIV_ayuda(ayuda)));


    var listaWrap = new Element("DIV", {"id":"lista_wrap"});
    $("detalles_nominado").insert(new Element("DIV", {"id":"lista_media"}).update(listaWrap));
    
    
    for(var j=0; j < media_len; j++){
        listaWrap.insert(new Element("DIV",{"class":"med_cont", "onclick":'cambiar_foto("'+media[j].id+'")'})
            .update(new Element("IMG",{"src":media[j], "height":"64"})));
    }

    ayuda = "No hay archivos multimedia para esta nominacion.<br>" +
    "Si tienes fotos o videos de esta/s persona/s contactanos al ceic@ldc.usb.ve";

    if(media_len <= 0) listaWrap.update(DIV_ayuda(ayuda));

}

function cambiar_foto(id) {
    if(media[id].esVideo) {
        $("vista_media").update("<div><iframe height='295' width='530' src='http://www.youtube.com/embed/"+media[id].url+"' frameborder='0' allowfullscreen></iframe><div>");
    } else {
        $("vista_media").update("<div><img src='"+media[id]+"' ><div>");
    }
    
}


function cambiar_categoria_votado(id, votado) {
    if(votado) {
        $("categoria"+id).removeClassName('no_votado');
        $("categoria"+id).addClassName('votado');
    } else {
        $("categoria"+id).removeClassName('votado');
        $("categoria"+id).addClassName('no_votado');
    }
}

function cambiar_nominado_votado(id, votado) {
    nominaciones[id].votado = votado;
    if(votado) {
        $("nominado"+id).removeClassName('no_votado');
        $("nominado"+id).addClassName('votado');
    } else {
        $("nominado"+id).removeClassName('votado');
        $("nominado"+id).addClassName('no_votado');
    }
}

function votar(nom_id){
    /* Como pueden haber interacciones entre votaciones de nominaciones de la misma
     * categoria hay que proteger las consultas con el flag AJAX_en_proceso, asi
     * no se podran hacer una consulta hasta que la anterior este resuelta.
     */
    while(AJAX_en_proceso) {}

    //Se decide si se agregara o se quitara el voto:
    var agregar   = !nominaciones[nom_id].votado,
        categoria = categoria_actual();

    if(agregar) {
        var nominado;
        //Si se va a agregar hay que revisar si ya hay un voto para la categoria.
        for(var i = 0; i < categoria.nominaciones.length; i++){
            nominado = categoria.nominaciones[i];
            if(nominado.votado && nominado.id != nom_id) {
                votar(nominado.id);
                break;
            }
        }
    }

    AJAX_en_proceso = true;
    /* Accion en JavaScript, estas acciones dependiendo de su exito o fracaso
     * continuaran el algoritmo para actualizar la interfaz.
     */
    if(agregar) {
        AJAX_Votar(nom_id);
    } else {
        AJAX_quitar_voto(nom_id, categoria_ind);
    }
}

function AJAX_Votar(nominacion_id){
    new Ajax.Request('/votar_do',
    {
        method:'post',
        parameters: {
            "id":nominacion_id
        },
        onSuccess: function(transport){
            if(transport.responseText === '1') {
                cambiar_categoria_votado(categoria_ind, true);

                cambiar_nominado_votado(nominacion_id, true);

                $("boton_votar").removeClassName('votar_si');
                $("boton_votar").addClassName('votar_no');
                $("boton_votar").update("Quitar Voto");
            } else {
                alert("Ocurrio un error en el servidor =s");
            }
            AJAX_en_proceso = false;
        },
        onFailure: function(){
            alert("No se pudo efectuar la votación, intente más tarde y verifique su conexión.");

            AJAX_en_proceso = false;
        }
    });
}

function AJAX_quitar_voto(nominacion_id, categoria_id){
    new Ajax.Request('/quitar_voto_do',
    {
        method:'post',
        parameters: {
            "id":categoria_id
        },
        onSuccess: function(transport){
            if(transport.responseText === '1') {
                cambiar_categoria_votado(categoria_ind, false);

                cambiar_nominado_votado(nominacion_id, false);

                $("boton_votar").removeClassName('votar_no');
                $("boton_votar").addClassName('votar_si');
                $("boton_votar").update("Votar");
            } else {
                alert("Ocurrio un error en el servidor =s");
            }

            AJAX_en_proceso = false;
        },
        onFailure: function(){
            alert("No se pudo remover el voto, intente más tarde y verifique su conexión.");

            AJAX_en_proceso = false;
        }
    });
}
