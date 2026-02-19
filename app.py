from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db, Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

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
            apaterno = alum1.apaterno
            email = alum1.email
            fecha = alum1.created_date
        else:
            nombre = ""
            apaterno = ""
            email = ""
            fecha = ""

        return render_template("detalles.html", nombre=nombre, apaterno=apaterno, email=email, fecha=fecha, id=id)
    
    return redirect(url_for('index'))

@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    form = forms.UserForm2(request.form)
    
    if request.method == 'POST' and form.validate():
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
            flash(f'Error al guardar: {str(e)}')
            print(f"Error: {e}")

    return render_template("Alumnos.html", form=form)

@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
    form = forms.UserForm2(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        form.id.data = request.args.get('id')
        form.nombre.data = alum1.nombre
        form.apaterno.data = alum1.apaterno
        form.email.data = alum1.email

    if request.method == 'POST':
        id = form.id.data
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum1.nombre = form.nombre.data
        alum1.apaterno = form.apaterno.data
        alum1.email = form.email.data
        
        db.session.add(alum1)
        db.session.commit()
        flash('Alumno actualizado correctamente')
        return redirect(url_for('index'))

    return render_template("modificar.html", form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)