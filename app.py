import os
import yagmail as yagmail
import functools
from werkzeug.utils import redirect
from flask import Flask, request, jsonify, url_for, g, session
from flask.templating import render_template
from forms import FormCalificar, FormCitas, FormContactanos, FormObservacion, FormSesion
from forms import FormRegistro
from models import paciente,citas

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)

#Decorador para verificar que el paciente es autenticado
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect( url_for('sesion') )

        return view(**kwargs)

    return wrapped_view

#Decorador para verificar que el paciente es autenticado
def login_required_medico(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.medic is None:
            return redirect( url_for('sesion_medico') )

        return view(**kwargs)

    return wrapped_view


@app.before_request
def cargar_usuario_autenticado():
    nombre_usuario = session.get('nombre_usuario')
    if nombre_usuario is None:
        g.user = None
    else:
        g.user = paciente.cargar(nombre_usuario)

@app.before_request
def cargar_medico_autenticado():
    nombre_usuario = session.get('nombre_usuario')
    if nombre_usuario is None:
        g.medic = None
    else:
        g.medic = paciente.cargar2(nombre_usuario)


@app.route('/')
def index():
    return render_template('layout.html')

@app.route("/logout/")
@login_required
def logout():
    session.clear()
    return redirect( url_for('sesion') )

@app.route("/logout2/")
@login_required_medico
def logout2():
    session.clear()
    return redirect( url_for('sesion_medico') )

@app.route('/sesion/', methods=["GET", "POST"])
def sesion():
    if request.method=="GET":
        return render_template('sesion.html', form=FormSesion())
    else:
        formulario = FormSesion(request.form)

        usr = formulario.nombre.data.replace("'","")
        pwd = formulario.contrasena.data.replace("'","")

        obj_usuario = paciente(usr,'','','',pwd)
        if obj_usuario.autenticar():
            session.clear()
            session["nombre_usuario"] = usr
            return redirect( url_for('usuario'))
        
        return render_template('sesion.html', mensaje="Nombre de usuario o contraseña incorrecta.", 
        form=formulario)

@app.route('/sesion-medico/', methods=["GET", "POST"])
def sesion_medico():
    if request.method=="GET":
        return render_template('sesion_medico.html', form=FormSesion())
    else:
        formulario = FormSesion(request.form)

        usr = formulario.nombre.data.replace("'","")
        pwd = formulario.contrasena.data.replace("'","")

        obj_usuario = paciente(usr,'','','',pwd)
        if obj_usuario.autenticar2():
            session.clear()
            session["nombre_usuario"] = usr
            return redirect( url_for('medico'))
        
        return render_template('sesion_medico.html', mensaje="Nombre de usuario o contraseña incorrecta.", 
        form=formulario)

@app.route('/registro/', methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        formulario = FormRegistro()
        return render_template('registro.html', form=formulario)
    else:
        formulario = FormRegistro(request.form)
        if formulario.validate_on_submit():
            obj_usuario = paciente(formulario.usuario.data, formulario.nombre.data, formulario.documento.data, formulario.correo.data, formulario.contrasena.data)
            if obj_usuario.insertar():
                #Aqui podrias agregar más adelante un código para enviar correo electrónico al usuario
                #y que pueda activar su cuenta.
                return render_template('registro.html', mensaje="Se registró el usuario exitosamente.", form=FormRegistro())

        return render_template('registro.html', mensaje="Todos los datos son obligatorios.", form=formulario)

@app.route('/admin/registro_medico/', methods=["GET", "POST"])
def registro_medico():
    if request.method == "GET":
        formulario = FormRegistro()
        return render_template('registro_medico.html', form=formulario)
    else:
        formulario = FormRegistro(request.form)
        if formulario.validate_on_submit():
            obj_usuario = paciente(formulario.usuario.data, formulario.nombre.data, formulario.documento.data, formulario.correo.data, formulario.contrasena.data)
            if obj_usuario.insertar2():
                #Aqui podrias agregar más adelante un código para enviar correo electrónico al usuario
                #y que pueda activar su cuenta.
                return render_template('registro_medico.html', mensaje="Se registró el usuario exitosamente.", form=FormRegistro())

        return render_template('registro_medico.html', mensaje="Todos los datos son obligatorios.", form=formulario)

@app.route('/sesion/usuario/', methods=["GET", "POST"])
@login_required
def usuario():
    nombre_usuario = session.get('nombre_usuario')
    return render_template('paciente.html', aver=session.get('nombre_usuario'))

@app.route('/sesion/medico/', methods=["GET", "POST"])
@login_required_medico
def medico():
        return render_template('medico.html', aver=session.get('nombre_usuario'))





@app.route('/sesion/medico/citas/observacion/', methods=["GET", "POST"])
@login_required
def comentario():
    nombre_usuario = session.get('nombre_usuario')
    if request.method == "GET":

        formulario = FormContactanos()
        return render_template('observacion.html', form=formulario,aver=nombre_usuario)

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
            return render_template('observacion.html',mensaje="Su mensaje ha sido enviado.", form=FormContactanos(), aver=session.get('nombre_usuario'))
            

        return render_template('observacion.html', mensaje="Todos los campos son obligatorios.", form=formulario, aver=nombre_usuario)
    
@app.route('/sesion/usuario/citas/', methods=["GET", "POST"])
@login_required
def cita():
    nombre_usuario = session.get('nombre_usuario')
    if request.method == "GET":

        formulario = FormCitas()
        return render_template('citas.html', form=formulario, aver=nombre_usuario)

    else:
        formulario = FormCitas(request.form)
        nombre_usuario = session.get('nombre_usuario')
        formulario.usuario.data= nombre_usuario
        if formulario.validate_on_submit():
            
            objeto_cita = citas( formulario.usuario.data, formulario.nombre.data,
            formulario.medico.data, formulario.fechas.data,None, None)

            #Invocamos el método insertar para guardar el mensaje en bd
            if objeto_cita.insertar3():
                yag = yagmail.SMTP('alertasmisiontic2022@gmail.com','prueba123')
                yag.send(to=formulario.correo.data,subject="Su mensaje ha sido recibido.",
                            contents="Hola {0}, hemos recibido tu mensaje. En breve nos comunicaremos contigo.".format(formulario.nombre.data))
                return render_template('citas.html',mensaje="Cita Registrada Con Exito.", form=FormCitas(), aver=session.get('nombre_usuario'))
            else:
                return render_template('citas.html', mensaje="La fecha y hora ya a sido asignada. Intente con una fecha nueva.", form=formulario, aver=nombre_usuario) 

        return render_template('citas.html', mensaje="Todos los campos son obligatorios.", form=formulario, aver=nombre_usuario)    

@app.route('/sesion/usuario/ver_citas/', methods=["GET"])
@login_required
def get_listado_mensajes():
    formulario = FormCitas(request.form)
    nombre_usuario = session.get('nombre_usuario')
    formulario.usuario.data = nombre_usuario
    objeto_cita = citas( formulario.usuario.data, None,None, None,None, None)
    if objeto_cita.listado():
        return render_template('lista_citas.html', lista=objeto_cita.listado(),aver=session.get('nombre_usuario'), form=FormCitas() )


@app.route('/sesion/usuario/ver_citas/<fecha>', methods=["GET"])
@login_required
def get_mensaje(fecha):
    nombre_usuario = session.get('nombre_usuario')
    objeto_mensaje = citas.cargar(fecha)
    if objeto_mensaje:
        return render_template('ver_mensaje.html',item=objeto_mensaje, aver=session.get('nombre_usuario'))
    
    return render_template('ver_mensaje.html', aver=nombre_usuario)

@app.route('/sesion/usuario/citas/calificar/<id_fecha>', methods=["GET", "POST"])
@login_required
def calificar_cita(id_fecha):
    nombre_usuario = session.get('nombre_usuario')
    if request.method == "GET":
        formulario = FormCalificar()

        objeto_cita = citas.cargar(id_fecha)
        if objeto_cita:
            formulario.usuario.data = objeto_cita.usuario
            formulario.nombre.data = objeto_cita.paciente
            formulario.medico.data = objeto_cita.doctor
            formulario.fechas.data = objeto_cita.fecha
            
            return render_template('calificar_cita.html',fecha= id_fecha, form = formulario, aver=session.get('nombre_usuario'))
        
        return render_template('calificar_cita.html',fecha= id_fecha, mensaje="No se encontraron citas programadas.", aver=nombre_usuario, formulario= FormCalificar())

    else:
        formulario = FormCalificar(request.form)
        if formulario.validate_on_submit():
            
            objeto_cita = citas.cargar(id_fecha)
            objeto_cita.calificacion = formulario.calificar.data
            objeto_cita.fecha = formulario.fechas.data
            objeto_calificar = citas (None,None,None,objeto_cita.fecha,None,objeto_cita.calificacion)
            if objeto_calificar.responder():
                yag = yagmail.SMTP('alertasmisiontic2022@gmail.com','prueba123')
                yag.send(to=formulario.correo.data,subject="Su Calificacion a sido enviada.",
                        contents="Hola {0}. Su calificacion es: {1}."
                        .format(formulario.nombre.data,  formulario.calificar.data))
                return render_template('calificar_cita.html',fecha=id_fecha, mensaje="Su Calificacion ha sido enviada.", aver=session.get('nombre_usuario'))
            else:
                return render_template('calificar_cita.html',fecha=id_fecha, form=formulario, 
                mensaje="No se pudo aregistrar su calificacion. Por favor intentelo nuevamente.", aver=nombre_usuario)

        return render_template('calificar_cita.html',fecha=id_fecha, form=formulario, mensaje="Todos los datos son obligatorios.",aver=nombre_usuario)



@app.route('/sesion/medico/ver_citas/', methods=["GET"])
@login_required_medico
def get_listado_mensajes_medico():
    formulario = FormRegistro(request.form)
    nombre_usuario = session.get('nombre_usuario')
    formulario.nombre.data = nombre_usuario
    obj_loco = paciente.cargar2(formulario.nombre.data)  
    formulario.documento.data = obj_loco.nombre 
    formulario.usuario.data = obj_loco.usuario
    objeto_cita = citas(  None,None,formulario.documento.data, None,None, None)
    if objeto_cita.listado2():
        return render_template('lista_medico.html',lista=objeto_cita.listado2(), aver=nombre_usuario, form=FormRegistro() )  
    #if obj_nombre.cargar_nombre():
        #aaa=obj_nombre.cargar_nombre()
        #formulario.usuario.data = aaa
        #return render_template('hola.html', form=formulario,jjj=formulario.usuario.data,tt=nombre_usuario, ll = formulario.documento.data)

@app.route('/sesion/medico/ver_citas/<fecha>', methods=["GET"])
@login_required_medico
def get_cita(fecha):
    nombre_usuario = session.get('nombre_usuario')
    objeto_mensaje = citas.cargar(fecha)
    

    if objeto_mensaje:
        return render_template('ver_citas.html',item=objeto_mensaje, aver=session.get('nombre_usuario'))
    
    return render_template('ver_citas.html', aver=nombre_usuario)

@app.route('/sesion/medico/citas/observaciones/<id_usuario>', methods=["GET", "POST"])
@login_required_medico
def get_observacion(id_usuario):
    nombre_usuario = session.get('nombre_usuario')
    if request.method == "GET":
        formulario = FormObservacion()

        objeto_cita = citas.cargar(id_usuario)
        if objeto_cita:
            formulario.usuario.data = objeto_cita.usuario
            formulario.nombre.data = objeto_cita.paciente
            formulario.medico.data = objeto_cita.doctor
            formulario.fechas.data = objeto_cita.fecha
            
            return render_template('observaciones.html',usuario= id_usuario, form = formulario, aver=session.get('nombre_usuario'))
        
        return render_template('observaciones.html',usuario= id_usuario, mensaje="No se encontraron citas programadas.", aver=nombre_usuario, formulario= FormObservacion())

    else:
        formulario = FormObservacion(request.form)
        if formulario.validate_on_submit():
            
            objeto_cita = citas.cargar(id_usuario)
            objeto_cita.observacion = formulario.observacion.data
            objeto_cita.fecha = formulario.fechas.data
            aa="bals_15@hotmail.com"
            objeto_calificar = citas (None,None,None,objeto_cita.fecha,objeto_cita.observacion,None)
            if objeto_calificar.responder():
                yag = yagmail.SMTP('alertasmisiontic2022@gmail.com','prueba123')
                yag.send(to=aa,subject="Su Calificacion a sido enviada.",
                        contents="Hola {0}. Su calificacion es: {1}."
                        .format(formulario.nombre.data,  formulario.observacion.data))
                return render_template('observaciones.html', item=objeto_calificar, usuario=id_usuario, mensaje="Su Calificacion ha sido enviada.", aver=session.get('nombre_usuario'))
            else:
                return render_template('observaciones.html',usuario=usuario,item=objeto_calificar, form=formulario, 
                mensaje="No se pudo aregistrar su calificacion. Por favor intentelo nuevamente.", aver=nombre_usuario)

        return render_template('observaciones.html',usuario=id_usuario, form=formulario, mensaje="Todos los datos son obligatorios.",aver=nombre_usuario)