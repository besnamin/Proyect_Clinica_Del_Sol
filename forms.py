from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.core import FloatField, RadioField, SelectField, StringField
from wtforms.fields.simple import PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField,TimeField

class FormSesion(FlaskForm):
    nombre = StringField('Usuario', validators=[validators.required(), validators.length(max=100)]) 
    contraseña = PasswordField('Password', validators=[validators.required(), validators.length(max=100)])
    enviar = SubmitField('Ingresar')

class FormRegistro(FlaskForm):
    nombre = StringField('Nombre completo', validators=[validators.required(), validators.length(max=100)]) 
    apellido = StringField('Apellido', validators=[validators.required(), validators.length(max=100)]) 
    documento = SelectField ('Tipo de documento', choices=[('Cedula de ciudadania'), ('T.I'), ('Cedula extranjera')], validators=[validators.required()])
    numero = FloatField ('No De Documento', validators=[validators.required(), validators.length(max=100)]) 
    enviar = SubmitField('Registrarse')

class FormContactanos(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[validators.required(), validators.length(max=100)]) 
    correo = StringField('Correo Electrónico', validators=[validators.required(), validators.length(max=150)])
    mensaje = TextAreaField('Mensaje', validators=[validators.required(), validators.length(max=500)])
    tipo = RadioField('Tipo de Mensaje', choices=[('P','Pregunta'),('Q','Queja'),('S','Sugerencia')])
    enviar = SubmitField('Enviar Mensaje')

class FormCitas(FlaskForm):
    medico = SelectField('Medico', choices=[('Juan Gabriel Espitia Gonzalez'), ('Rafael Eduardo Martinez Perez'), ('Jose Manuel Torres Alvarado3')], validators=[validators.required()])
    fecha = DateField('Ingrese La Fecha', format='%Y-%m-%d')
    hora = TimeField('ingrese la hora')
    enviar = SubmitField('Agendar Cita')