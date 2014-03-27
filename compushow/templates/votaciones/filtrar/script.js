function nominar() {

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
