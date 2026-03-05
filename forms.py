from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, TextAreaField, SelectField, validators

class Alumno(FlaskForm):
    id = IntegerField('id', [validators.Optional()])
    nombre = StringField("nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=50, message="Mínimo 4 y máximo 50 caracteres")
    ])
    apellidos = StringField("apellidos", [
        validators.DataRequired(message="Los apellidos son requeridos")
    ])
    email = EmailField("correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese un email válido")
    ])
    telefono = StringField("telefono", [
        validators.DataRequired(message="El teléfono es requerido"),
        validators.Regexp(r'^\d+$', message="El teléfono solo debe contener números"),
        validators.Length(min=10, max=10, message="El teléfono debe tener exactamente 10 dígitos")
    ])

class Maestro(FlaskForm):
    matricula = IntegerField('matricula', [validators.Optional()])
    nombre = StringField("nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=50, message="Mínimo 4 y máximo 50 caracteres")
    ])
    apellidos = StringField("apellidos", [
        validators.DataRequired(message="Los apellidos son requeridos")
    ])
    especialidad = StringField("especialidad", [
        validators.DataRequired(message="La especialidad es requerida")
    ])
    email = EmailField("correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese un email válido")
    ])

class Curso(FlaskForm):
    id = IntegerField('id', [validators.Optional()])
    nombre = StringField("nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=150, message="Mínimo 4 y máximo 150 caracteres")
    ])
    descripcion = TextAreaField("descripcion", [
        validators.Optional()
    ])
    maestro_id = SelectField("maestro", coerce=int, validators=[
        validators.DataRequired(message="Debe seleccionar un maestro")
    ])

class Inscripcion(FlaskForm):
    alumno_id = SelectField("alumno", coerce=int, validators=[
        validators.DataRequired(message="Debe seleccionar un alumno")
    ])
    curso_id = SelectField("curso", coerce=int, validators=[
        validators.DataRequired(message="Debe seleccionar un curso")
    ])