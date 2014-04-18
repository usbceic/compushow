
function validar_carnet(campo) {
    var carnet_regexp = new RegExp(/^\d{2}-\d{5}$/)
    return carnet_regexp.test(campo.value)
}

function validar_username(campo) {
    var username_regexp = new RegExp(/^.{4,11}$/)
    return username_regexp.test(campo.value)
}

function validar_correo(campo) {
    var correo_regexp = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i)
    return correo_regexp.test(campo.value);
}

function verificacion_registro() {

    estudiante = document.getElementById("es_estudiante");
    tipo_usuario = document.getElementById("tipo_usuario");
    if(estudiante.checked === true){
        carnet_bool = validar_carnet($("username"));
    }
    else{
        carnet_bool = validar_username($("username"));
    }

    $("carnet_ok").className = "indicador"+(carnet_bool?"Ok":"Ko");

    correo_bool = validar_correo($("Email"));

    $("correo_ok").className = "indicador"+(correo_bool?"Ok":"Ko");

    password_bool = $("password0").value.length > 0 && ($("password0").value == $("password").value);

    $("pass_ok").className = "indicador"+(password_bool?"Ok":"Ko");

    $("iniciar_btn").disabled = !(carnet_bool&&correo_bool&&password_bool);
}

function verificacion_login() {
    if($("usernameL").value.length> 0 && $("passwordL").value.length>0){
        $("iniciar_btnLog").disabled = false;
    }
    else{
        $("iniciar_btnLog").disabled = true;
    }  
}

function cambiarTipo(){
    estudiante = document.getElementById("es_estudiante");
    tipo_usuario = document.getElementById("tipo_usuario");
    if(estudiante.checked === true){
        tipo_usuario.update("Carnet");
    }
    else{
        tipo_usuario.update("Usuario");
    }
    verificacion_registro();

}