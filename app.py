from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db, Alumnos

app = Flask(__name__)

# 1. Configuración PRIMERO
app.config.from_object(DevelopmentConfig)

# 2. Inicializar extensiones DESPUÉS de la configuración
csrf = CSRFProtect(app)
db.init_app(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
@app.route("/index")
def index():
    try:
        lista_alumnos = Alumnos.query.all()
    except Exception as e:
        print(f"Error BD: {e}")
        lista_alumnos = []
    return render_template("index.html", alumnos=lista_alumnos)

@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    form = forms.UserForm2() # FlaskForm toma request.form automáticamente
    
    if request.method == 'POST':
        if form.validate_on_submit(): # Valida Token CSRF y datos
            try:
                alu = Alumnos(
                    nombre=form.nombre.data,
                    apaterno=form.apaterno.data,
                    email=form.email.data
                )
                db.session.add(alu)
                db.session.commit()
                flash('Alumno registrado correctamente')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                print(f"Error MySQL: {e}")
                flash('Error al guardar en la base de datos')
        else:
            # Si falla la validación, imprime los errores en consola para depurar
            print("Errores de validación:", form.errors)

    return render_template("Alumnos.html", form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)