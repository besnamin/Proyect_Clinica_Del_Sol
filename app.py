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

#Decorador para verificar que el paciente es autenticado
def login_required_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect( url_for('sesion_admin') )

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

@app.before_request
def cargar_admin_autenticado():
    nombre_usuario = session.get('nombre_usuario')
    if nombre_usuario is None:
        g.admin = None
    else:
        g.admin = paciente.cargaradmin(nombre_usuario)


@app.route('/')
def index():
    return render_template('layout.html')

@app.route("/logout/")
@login_required
def logout():
    session.clear()
    return redirect( url_for('index') )

@app.route("/logout2/")
@login_required_medico
def logout2():
    session.clear()
    return redirect( url_for('index') )

@app.route("/logout3/")
@login_required_admin
def logout3():
    session.clear()
    return redirect( url_for('index') )

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

@app.route('/sesion-admin/', methods=["GET", "POST"])
def sesion_admin():
    if request.method=="GET":
        return render_template('sesion_admin.html', form=FormSesion())
    else:
        formulario = FormSesion(request.form)

        usr = formulario.nombre.data.replace("'","")
        pwd = formulario.contrasena.data.replace("'","")

        obj_usuario = paciente(usr,'','','',pwd)
        if obj_usuario.autenticar3():
            session.clear()
            session["nombre_usuario"] = usr
            return redirect( url_for('admin'))
        
        return render_template('sesion_admin.html', mensaje="Nombre de usuario o contraseña incorrecta.", 
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
            return render_template('registro.html', mensaje="El nombre de usuario ya existe,pruebe con otro.", form=formulario)
        return render_template('registro.html', mensaje="Todos los datos son obligatorios.", form=formulario)

@app.route('/sesion/administrador/registro_medico/', methods=["GET", "POST"])
@login_required_medico
def registro_medico():
    if request.method == "GET":
        formulario = FormRegistro()
        return render_template('registro_medico.html', form=formulario )
    else:
        nombre_usuario = session.get('nombre_usuario') 
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

@app.route('/sesion/administrador/', methods=["GET", "POST"])
@login_required_admin
def admin():
        return render_template('administrador.html', aver=session.get('nombre_usuario'))

@app.route('/sesion/administrador/citas/', methods=["GET"])
@login_required_admin
def get_todas_citas():
    return render_template('todas_citas.html', lista=citas.listado3(),aver=session.get('nombre_usuario'))

@app.route('/sesion/administrador/pacientes/', methods=["GET"])
@login_required_admin
def ver_pacientes():
    return render_template('ver_pacientes.html', lista=citas.listado4(),aver=session.get('nombre_usuario'))

@app.route('/sesion/administrador/medicos/', methods=["GET"])
@login_required_admin
def ver_medicos():
    return render_template('ver_medicos.html', lista=citas.listado5(),aver=session.get('nombre_usuario'))

@app.route('/registro/', methods=["GET", "POST"])

@app.route('/admin/registrar/', methods=["GET", "POST"])
@login_required_admin
def registrar():
    nombre_usuario = session.get('nombre_usuario')
    if request.method == "GET":
        formulario = FormRegistro()
        return render_template('registro_medico.html', form=formulario, aver=nombre_usuario)
    else:
        formulario = FormRegistro(request.form)
        if formulario.validate_on_submit():
            obj_usuario = paciente(formulario.usuario.data, formulario.nombre.data, formulario.documento.data, formulario.correo.data, formulario.contrasena.data)
            if obj_usuario.insertar2():
                #Aqui podrias agregar más adelante un código para enviar correo electrónico al usuario
                #y que pueda activar su cuenta.
                return render_template('registro_medico.html', mensaje="Se registró el medico exitosamente.", form=FormRegistro(), aver =session.get('nombre_usuario'))

        return render_template('registro_medico.html', mensaje="Todos los datos son obligatorios.", form=formulario, aver=nombre_usuario)


    
@app.route('/sesion/usuario/citas/', methods=["GET", "POST"])
@login_required
def cita():
    nombre_usuario = session.get('nombre_usuario')
    if request.method == "GET":

        formulario = FormCitas()
        formulario.usuario.data=nombre_usuario
        objeto_nombre = paciente.cargar_nombre3(formulario.usuario.data)
        if objeto_nombre:
            formulario.nombre.data=objeto_nombre.nombre
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
    else: 
         return render_template('paciente.html', mensaje="Aun no tiene citas programadas", aver=session.get('nombre_usuario')) 

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
    else: 
         return render_template('medico.html', mensaje="Aun no tiene citas Asignadas Para Atender", aver=session.get('nombre_usuario')) 
    

@app.route('/sesion/medico/ver_citas/<fecha>', methods=["GET"])
@login_required_medico
def get_cita(fecha):
    nombre_usuario = session.get('nombre_usuario')
    objeto_mensaje = citas.cargar(fecha)
    

    if objeto_mensaje:
        return render_template('ver_citas.html',item=objeto_mensaje, aver=session.get('nombre_usuario'))
    
    return render_template('ver_citas.html', aver=nombre_usuario)

@app.route('/sesion/medico/ver_citas/observacion/', methods=["GET"])
@login_required_medico
def get_listado_mensajes_medico2():
    formulario = FormRegistro(request.form)
    nombre_usuario = session.get('nombre_usuario')
    formulario.nombre.data = nombre_usuario
    obj_loco = paciente.cargar2(formulario.nombre.data)  
    formulario.documento.data = obj_loco.nombre 
    formulario.usuario.data = obj_loco.usuario
    objeto_cita = citas(  None,None,formulario.documento.data, None,None, None)
    if objeto_cita.listado2():
        return render_template('lista_medico2.html',lista=objeto_cita.listado2(), aver=nombre_usuario ) 

@app.route('/sesion/medico/citas/observaciones/<fecha>', methods=["GET", "POST"])
@login_required_medico
def get_observacion(fecha):
    nombre_usuario = session.get('nombre_usuario')
    if request.method == "GET":
        formulario = FormObservacion()

        objeto_cita = citas.cargar(fecha)
        if objeto_cita:
            formulario.usuario.data = objeto_cita.usuario
            formulario.nombre.data = objeto_cita.paciente
            formulario.medico.data = objeto_cita.doctor
            formulario.fechas.data = objeto_cita.fecha
            
            return render_template('observaciones.html',usuario= fecha, form = formulario, aver=session.get('nombre_usuario'))
        
        return render_template('observaciones.html',usuario= fecha, mensaje="No se encontraron citas programadas.", aver=nombre_usuario, formulario= FormObservacion())

    else:
        formulario = FormObservacion(request.form)
        if formulario.validate_on_submit():
            
            objeto_cita = citas.cargar(fecha)
            objeto_cita.observacion = formulario.observacion.data
            
            
            objeto_calificar = citas (None,None,None,objeto_cita.fecha,objeto_cita.observacion,None)
            if objeto_calificar.responder2():
                
                return render_template('observaciones.html', item=objeto_calificar, usuario=fecha, mensaje="Su Observacion ha sido enviada.", aver=session.get('nombre_usuario'))
            else:
                return render_template('observaciones.html',usuario=usuario,item=objeto_calificar, form=formulario, 
                mensaje="No se pudo aregistrar su calificacion. Por favor intentelo nuevamente.", aver=nombre_usuario)

        return render_template('observaciones.html',usuario=fecha, form=formulario, mensaje="Todos los datos son obligatorios.",aver=nombre_usuario)