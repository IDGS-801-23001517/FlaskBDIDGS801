from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, PasswordField, FloatField
from wtforms import EmailField
from wtforms import validators

class UserForm2(Form):
     
    id=IntegerField('id',
    [validators.number_range(min=1, max=20, message='Valor no valido')])

    nombre=StringField("nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=4, max=20, message="Ingrese nombre valido, minimo 4 y maximo 20 caracteres")])
    
    apaterno=StringField("apaterno", [
        validators.DataRequired(message="El apellido es requerido")])
    
    matricula=IntegerField("Matricula", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=100, max=1000, message="Ingrese valor valido")])
    
    email=EmailField("correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese un email valido")])

    
    