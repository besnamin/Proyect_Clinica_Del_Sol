import os
import yagmail as yagmail

from flask import Flask, request
from flask.templating import render_template
from forms import FormSesion
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
            
            return render_template('sesion.html',mensaje="Bienvenido", form=FormSesion())

        return render_template('sesion.html', mensaje="Todos los campos son obligatorios.", form=formulario)

@app.route('/registro/', methods=["GET", "POST"])
def registro():
    formulario = FormRegistro()
    return render_template('registro.html', form=formulario)