from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db, Alumnos
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
migrate = Migrate(app, db)

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

@app.route("/detalles", methods=['GET', 'POST'])
def detalles():
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        
        if alum1:
            nombre = alum1.nombre
            apellidos = alum1.apellidos
            email = alum1.email
            telefono = alum1.telefono
            fecha = alum1.created_date
        else:
            nombre = ""
            apellidos = ""
            email = ""
            fecha = ""

        return render_template("detalles.html", nombre=nombre, apellidos=apellidos, email=email, telefono=telefono, fecha=fecha, id=id)
    
    return redirect(url_for('index'))

@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    form = forms.UserForm2(request.form)
    
    if request.method == 'POST' and form.validate():
        try:
            alu = Alumnos(
                nombre=form.nombre.data,
                apellidos=form.apellidos.data,
                email=form.email.data,
                telefono=form.telefono.data
            )
            db.session.add(alu)
            db.session.commit()
            flash('Alumno registrado correctamente')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar: {str(e)}')
            print(f"Error: {e}")

    return render_template("Alumnos.html", form=form)

@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
    form = forms.UserForm2(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alumno:
            form.id.data = alumno.id
            form.nombre.data = alumno.nombre
            form.apellidos.data = alumno.apellidos
            form.email.data = alumno.email
            form.telefono.data = alumno.telefono
        else:
            flash('Alumno no encontrado')
            return redirect(url_for('index'))

    if request.method == 'POST' and form.validate():
        try:
            id = form.id.data
            alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
            if alumno:
                alumno.nombre = form.nombre.data
                alumno.apellidos = form.apellidos.data
                alumno.email = form.email.data
                alumno.telefono = form.telefono.data
                
                db.session.commit()
                flash('Alumno actualizado correctamente')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}')

    return render_template("modificar.html", form=form)

@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    form = forms.UserForm2(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alumno:
            form.id.data = alumno.id
            form.nombre.data = alumno.nombre
            form.apellidos.data = alumno.apellidos
            form.email.data = alumno.email
            form.telefono.data = alumno.telefono
        else:
            flash('Alumno no existe')
            return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            id = form.id.data
            alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
            if alumno:
                db.session.delete(alumno)
                db.session.commit()
                flash('Registro eliminado exitosamente')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al eliminar: {str(e)}')

    return render_template("eliminar.html", form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)