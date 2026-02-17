from flask_wtf import FlaskForm # <-- CAMBIO IMPORTANTE
from wtforms import StringField, IntegerField, EmailField, validators

class UserForm2(FlaskForm): # <-- AHORA HEREDA DE FlaskForm
    
    id = IntegerField('id', [
        validators.Optional()
    ])

    nombre = StringField("nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=20, message="Mínimo 4 y máximo 20 caracteres")
    ])
    
    apaterno = StringField("apaterno", [
        validators.DataRequired(message="El apellido es requerido")
    ])
    
    # Matricula opcional según tu html
    matricula = IntegerField("Matricula", [
        validators.Optional(),
        validators.NumberRange(min=100, max=100000, message="Ingrese valor válido")
    ])
    
    email = EmailField("correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese un email válido")
    ])