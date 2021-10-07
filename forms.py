from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.core import FloatField, SelectField, StringField
from wtforms.fields.simple import PasswordField, SubmitField, TextAreaField

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