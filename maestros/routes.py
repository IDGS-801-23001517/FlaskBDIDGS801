from . import maestros
from flask import render_template, request, redirect, url_for, flash
from models import db, Maestros
import forms

@maestros.route("/maestros")
def index():
    try:
        lista_maestros = Maestros.query.all()
    except Exception as e:
        print(f"Error BD: {e}")
        lista_maestros = []
    return render_template("maestros/maestros.html", maestros=lista_maestros)

@maestros.route("/maestros/detalles", methods=['GET', 'POST'])
def detalles():
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        
        if maestro:
            nombre = maestro.nombre
            apellidos = maestro.apellidos
            especialidad = maestro.especialidad
            email = maestro.email
        else:
            nombre = apellidos = especialidad = email = ""

        return render_template("maestros/detalles.html", nombre=nombre, apellidos=apellidos, especialidad=especialidad, email=email, matricula=matricula)
    
    return redirect(url_for('maestros.index'))

@maestros.route("/maestros/agregar", methods=['GET', 'POST'])
def agregar():
    form = forms.Maestro(request.form)
    
    if request.method == 'POST' and form.validate():
        try:
            maestro = Maestros(
                nombre=form.nombre.data,
                apellidos=form.apellidos.data,
                especialidad=form.especialidad.data,
                email=form.email.data
            )
            db.session.add(maestro)
            db.session.commit()
            flash('Maestro registrado correctamente')
            return redirect(url_for('maestros.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar: {str(e)}')
            print(f"Error: {e}")

    return render_template("maestros/agregar.html", form=form)

@maestros.route("/maestros/modificar", methods=['GET', 'POST'])
def modificar():
    form = forms.Maestro(request.form)
    
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maestro:
            form.matricula.data = maestro.matricula
            form.nombre.data = maestro.nombre
            form.apellidos.data = maestro.apellidos
            form.especialidad.data = maestro.especialidad
            form.email.data = maestro.email
        else:
            flash('Maestro no encontrado')
            return redirect(url_for('maestros.index'))

    if request.method == 'POST' and form.validate():
        try:
            matricula = form.matricula.data
            maestro = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
            if maestro:
                maestro.nombre = form.nombre.data
                maestro.apellidos = form.apellidos.data
                maestro.especialidad = form.especialidad.data
                maestro.email = form.email.data
                
                db.session.commit()
                flash('Maestro actualizado correctamente')
            return redirect(url_for('maestros.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}')

    return render_template("maestros/modificar.html", form=form)

@maestros.route('/maestros/eliminar', methods=['GET', 'POST'])
def eliminar():
    form = forms.Maestro(request.form)
    
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maestro:
            form.matricula.data = maestro.matricula
            form.nombre.data = maestro.nombre
            form.apellidos.data = maestro.apellidos
            form.especialidad.data = maestro.especialidad
            form.email.data = maestro.email
        else:
            flash('Maestro no existe')
            return redirect(url_for('maestros.index'))

    if request.method == 'POST':
        try:
            matricula = form.matricula.data
            maestro = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
            if maestro:
                db.session.delete(maestro)
                db.session.commit()
                flash('Registro eliminado exitosamente')
            return redirect(url_for('maestros.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al eliminar: {str(e)}')

    return render_template("maestros/eliminar.html", form=form)