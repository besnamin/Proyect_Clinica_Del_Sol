import os
import yagmail as yagmail

from flask import Flask, request
from flask.templating import render_template
from forms import FormCitas, FormContactanos, FormSesion
from forms import FormRegistro

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/sesion/', methods=["GET", "POST"])
def sesion():
    if request.method == "GET":
        formulario = FormSesion()
        return render_template('sesion.html', form=formulario)
    else:
        formulario = FormSesion(request.form)
        if formulario.validate_on_submit():
            
            return render_template('paciente.html')

        return render_template('sesion.html', mensaje="Todos los campos son obligatorios.", form=formulario)

@app.route('/registro/', methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        formulario = FormRegistro()
        return render_template('registro.html', form=formulario)
    else:
        formulario = FormRegistro(request.form)
        if formulario.validate_on_submit():
             return render_template('sesion.html',mensaje="Bienvenido", form=FormSesion())

        return render_template('registro.html', mensaje="Todos los campos son obligatorios.", form=formulario)

@app.route('/sesion/usuario/', methods=["GET", "POST"])
def usuario():
        return render_template('paciente.html')

@app.route('/sesion/medico/', methods=["GET", "POST"])
def medico():
        return render_template('medico.html')

@app.route('/sesion/medico/citas', methods=["GET", "POST"])
def citas_progamadas():
        return render_template('lista_citas.html')

@app.route('/sesion/medico/comentarios', methods=["GET", "POST"])
def ver_comentarios():
        return render_template('ver_comentarios.html')



@app.route('/sesion/usuario/comentario/', methods=["GET", "POST"])
def comentario():
    if request.method == "GET":

        formulario = FormContactanos()
        return render_template('comentario.html', form=formulario)

    else:
        formulario = FormContactanos(request.form)
        if formulario.validate_on_submit():
            
            #Instanciamos la clase mensaje con los datos 
            #del formulario que se reciben de la petición
            #objeto_mensaje = mensaje(0, formulario.nombre.data,
            #formulario.correo.data, formulario.mensaje.data, None, 'S')

            #Invocamos el método insertar para guardar el mensaje en bd
            #if objeto_mensaje.insertar():
            yag = yagmail.SMTP('alertasmisiontic2022@gmail.com','prueba123')
            yag.send(to=formulario.correo.data,subject="Su mensaje ha sido recibido.",
                        contents="Hola {0}, hemos recibido tu mensaje. En breve nos comunicaremos contigo.".format(formulario.nombre.data))
            return render_template('comentario.html',mensaje="Su mensaje ha sido enviado.", form=FormContactanos())
            

        return render_template('comentario.html', mensaje="Todos los campos son obligatorios.", form=formulario)
    
@app.route('/sesion/usuario/citas/', methods=["GET", "POST"])
def cita():
    if request.method == "GET":

        formulario = FormCitas()
        return render_template('citas.html', form=formulario)

    else:
        formulario = FormCitas(request.form)
        if formulario.validate_on_submit():
            
            #Instanciamos la clase mensaje con los datos 
            #del formulario que se reciben de la petición
            #objeto_mensaje = mensaje(0, formulario.nombre.data,
            #formulario.correo.data, formulario.mensaje.data, None, 'S')

            #Invocamos el método insertar para guardar el mensaje en bd
            #if objeto_mensaje.insertar():
            yag = yagmail.SMTP('alertasmisiontic2022@gmail.com','prueba123')
            yag.send(to=formulario.correo.data,subject="Su mensaje ha sido recibido.",
                        contents="Hola {0}, hemos recibido tu mensaje. En breve nos comunicaremos contigo.".format(formulario.nombre.data))
            return render_template('citas.html',mensaje="Su mensaje ha sido enviado.", form=FormCitas())
            

        return render_template('citas.html', mensaje="Todos los campos son obligatorios.", form=formulario)


