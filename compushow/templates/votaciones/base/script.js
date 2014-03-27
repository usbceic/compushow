function DIV_ayuda(texto) {
    return new Element("DIV", {"class":"ayuda"}).update(texto).insert(new Element("DIV", {"id":"icono_ayuda"}));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

Ajax.Base.prototype.initialize = Ajax.Base.prototype.initialize.wrap(
    function (callOriginal, options) {
        var headers = options.requestHeaders || {};
        headers["X-CSRFToken"] = getCookie("csrftoken");
        options.requestHeaders = headers;
        return callOriginal(options);
    }
    );