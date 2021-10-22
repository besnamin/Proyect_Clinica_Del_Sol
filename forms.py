from random import choice
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.core import  RadioField, SelectField, StringField
from wtforms.fields.simple import PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField, DateTimeLocalField,TimeField,DateTimeField
from wtforms.widgets.html5 import DateTimeInput, DateTimeLocalInput

class FormSesion(FlaskForm):
    nombre = StringField('Usuario', validators=[validators.required(), validators.length(max=100)]) 
    contrasena = PasswordField('Password', validators=[validators.required(), validators.length(max=100)])
    enviar = SubmitField('Ingresar')

class FormRegistro(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[validators.required(), validators.length(max=100)]) 
    nombre= StringField('Nombre Completo', validators=[validators.required(), validators.length(max=100)]) 
    documento = StringField ('Numero de cocumento', validators=[validators.required(), validators.length(max=100)])
    correo = StringField('Correo', validators=[validators.required(), validators.length(max=100)]) 
    contrasena = PasswordField('Contraseña', validators=[validators.required(), validators.length(max=100)]) 
    enviar = SubmitField('Registrarse')

class FormContactanos(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[validators.required(), validators.length(max=100)]) 
    correo = StringField('Correo Electrónico', validators=[validators.required(), validators.length(max=150)])
    mensaje = TextAreaField('Mensaje', validators=[validators.required(), validators.length(max=500)])
    tipo = RadioField('Tipo de Mensaje', choices=[('P','Pregunta'),('Q','Queja'),('S','Sugerencia')])
    enviar = SubmitField('Enviar Mensaje')

class FormCitas(FlaskForm):
    usuario = StringField('Nombre De Usuario', validators=[validators.required(), validators.length(max=100)])
    nombre = StringField('Nombre Completo', validators=[validators.required(), validators.length(max=100)])
    medico = SelectField (u'Medico',choices=[('Juan Gabriel Espitia Gonzalez', 'Juan Espitia Gonzalez'),('Rafael Eduardo Martinez Perez', 'Rafael Martinez Perez'),('Jose Manuel Torres Alvarado','Jose Torres Alvarado')],coerce=str,validators=[validators.optional()])
    fechas = DateTimeLocalField('Fecha y Hora', default='', format='%Y-%m-%dT%H:%M')
    correo = StringField('Correo Electrónico', validators=[validators.required(), validators.length(max=150)])
    enviar = SubmitField('Agendar Cita')

class FormCalificar(FlaskForm):
    usuario = StringField('Nombre De Usuario', validators=[validators.required(), validators.length(max=100)])
    nombre = StringField('Nombre Completo', validators=[validators.required(), validators.length(max=100)])
    medico = StringField('Medico', validators=[validators.required(), validators.length(max=100)])
    fechas = StringField('Fecha y Hora', validators=[validators.required(), validators.length(max=100)])
    correo = StringField('Correo Electrónico', validators=[validators.required(), validators.length(max=150)])
    calificar = SelectField (u'Califique su cita.(5 max- 1 min)',choices=[(1, '1'),(2, '2'),(3,'3'),(4, '4'),(5,'5')],coerce=int,validators=[validators.optional()])
    enviar = SubmitField('Calificar Cita')

class FormObservacion(FlaskForm):
    usuario = StringField('Nombre De Usuario', validators=[validators.required(), validators.length(max=100)])
    nombre = StringField('Nombre Completo', validators=[validators.required(), validators.length(max=100)])
    medico = StringField('Medico', validators=[validators.required(), validators.length(max=100)])
    fechas = StringField('Fecha y Hora', validators=[validators.required(), validators.length(max=100)])
    observacion = TextAreaField('Observaciones', validators=[validators.required(), validators.length(max=500)])
    enviar = SubmitField('Enviar Observacion')
    