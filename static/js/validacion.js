function validar_formulario() {
    
    var nombre = document.getElementById('nombre');
    var usuario = document.getElementById('usuario');
    var email = document.getElementById('correo');
    var password = document.getElementById('contrasena');
    var documento = document.getElementById('documento')
    var parrafo_errores = document.getElementById('errores');
    var hay_errores = false;
    parrafo_errores.innerHTML = "";
    if (nombre.value == "" || nombre.value.length < 8) {
        //alert('El nombre no cumple con los requisitos mínimos.');
        parrafo_errores.innerHTML += 'El nombre no cumple con los requisitos mínimos,debe contener mas de 8 careacteres.<br>';
        //return false;
        hay_errores = true
    }

    if (usuario.value == "" || usuario.value.length < 4) {
        //alert('El usuario no cumple con los requisitos mínimos.');
        parrafo_errores.innerHTML += 'El usuario no cumple con los requisitos mínimos,debe contener mas de 4 elementos.<br>';
        //return false;
        hay_errores = true;
    }

    if (documento.value == "" || documento.value.length < 8) {
        //alert('El usuario no cumple con los requisitos mínimos.');
        parrafo_errores.innerHTML += 'El documento debe contener mas de 8 elementos.<br>';
        //return false;
        hay_errores = true;
    }

    var expresion = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/;
    if (!email.value.match(expresion)) {
        //alert('El correo electrónico es inválido.');
        parrafo_errores.innerHTML += 'El correo electrónico es inválido.<br>';
        //return false;
        hay_errores = true;
    } 

    if (password.value == "" || password.value.length < 8) {
        //alert('El password no cumple con los requisitos mínimos.');
        parrafo_errores.innerHTML += 'La Contraseña debe contener mas de 8 elementos.<br>'
        hay_errores = true;
        //return false;
    }
    
    if (hay_errores==true){
        alert('Se encontraron errores en el formulario, por favor verifique.');
    }
    return !hay_errores;  

}

function isNumberKey(evt){
    var charCode = (evt.which) ? evt.which : evt.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}

function validar_formulario_sesion() {
    
    var nombre = document.getElementById('nombre');
    var password = document.getElementById('contrasena');
    var parrafo_errores = document.getElementById('errores');
    var hay_errores = false;
    parrafo_errores.innerHTML = "";
    if (nombre.value == "" ) {
        //alert('El nombre no cumple con los requisitos mínimos.');
        parrafo_errores.innerHTML += 'Ingresa un nombre usuario.<br>';
        //return false;
        hay_errores = true
    }


    if (password.value == "" || password.value.length < 8) {
        //alert('El password no cumple con los requisitos mínimos.');
        parrafo_errores.innerHTML += 'Ingresa una contraseña.<br>'
        hay_errores = true;
        //return false;
    }  

}

function validar_formulario_cita() {
    var fecha = document.getElementById('fechas')
    var email = document.getElementById('correo');
    var parrafo_errores = document.getElementById('errores');
    var hay_errores = false;
    parrafo_errores.innerHTML = "";

    var expresion = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/;
    if (!email.value.match(expresion)) {
        //alert('El correo electrónico es inválido.');
        parrafo_errores.innerHTML += 'El correo electrónico es inválido.<br>';
        //return false;
        hay_errores = true;
    } else{
        hay_errores = false
    }

    if (fecha.value == "" ) {
        //alert('El password no cumple con los requisitos mínimos.');
        parrafo_errores.innerHTML += 'Debe Ingresar una Fecha.<br>'
        hay_errores = true;
        //return false;
    }else{
        hay_errores = false
    }
    
    if (hay_errores==true){
        alert('Se encontraron errores en el formulario, por favor verifique.');
    }
    return !hay_errores;        

}

function validar_formulario_calificacion() {
    var email = document.getElementById('correo');
    var parrafo_errores = document.getElementById('errores');
    var hay_errores = false;
    parrafo_errores.innerHTML = "";

    var expresion = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/;
    if (!email.value.match(expresion)) {
        //alert('El correo electrónico es inválido.');
        parrafo_errores.innerHTML += 'El correo electrónico es inválido.<br>';
        //return false;
        hay_errores = true;
    } 

    
    if (hay_errores==true){
        alert('Se encontraron errores en el formulario, por favor verifique.');
    }
    return !hay_errores;        

}

function validar_formulario_observacion() {
    
    var observacion = document.getElementById('observacion');
    var parrafo_errores = document.getElementById('errores');
    var hay_errores = false;
    parrafo_errores.innerHTML = "";
    if (observacion.value == "" ) {
        //alert('El nombre no cumple con los requisitos mínimos.');
        parrafo_errores.innerHTML += 'Ingresa un nombre usuario.<br>';
        //return false;
        hay_errores = true
    }


    

}