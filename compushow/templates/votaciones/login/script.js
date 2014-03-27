
function validar_carnet(campo) {
    var carnet_regexp = new RegExp(/^\d{2}-\d{5}$/)
    return carnet_regexp.test(campo.value)
}

function validar_correo(campo) {
    var correo_regexp = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i)
    return correo_regexp.test(campo.value);
}

function verificacion_registro() {
    
    carnet_bool = validar_carnet($("username"));
    
    $("carnet_ok").className = "indicador"+(carnet_bool?"Ok":"Ko");

    correo_bool = validar_correo($("Email"));

    $("correo_ok").className = "indicador"+(correo_bool?"Ok":"Ko");

    password_bool = $("password0").value.length > 0 && ($("password0").value == $("password").value);

    $("pass_ok").className = "indicador"+(password_bool?"Ok":"Ko");

    $("iniciar_btn").disabled = !(carnet_bool&&correo_bool&&password_bool);
}