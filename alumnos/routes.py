from . import alumnos
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Alumnos
import forms


@alumnos.route("/alumnos")
def index():
    try:
        lista_alumnos = Alumnos.query.all()
    except Exception as e:
        print(f"Error BD: {e}")
        lista_alumnos = []
    return render_template("alumnos/alumnos.html", alumnos=lista_alumnos)

@alumnos.route("/alumnos/detalles", methods=['GET', 'POST'])
def detalles():
    if request.method == 'GET':
        id = request.args.get('id')
        alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        
        if alumno:
            nombre = alumno.nombre
            apellidos = alumno.apellidos
            email = alumno.email
            telefono = alumno.telefono
            fecha = alumno.created_date
        else:
            nombre = ""
            apellidos = ""
            email = ""
            fecha = ""

        return render_template("alumnos/detalles.html", nombre=nombre, apellidos=apellidos, email=email, telefono=telefono, fecha=fecha, id=id)
    
    return redirect(url_for('alumnos/alumnos.html'))



@alumnos.route("/alumnos/agregar", methods=['GET', 'POST'])
def agregar():
    form = forms.Alumno(request.form)
    
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
            return redirect(url_for('alumnos.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar: {str(e)}')
            print(f"Error: {e}")

    return render_template("alumnos/agregar.html", form=form)

@alumnos.route("/alumnos/modificar", methods=['GET', 'POST'])
def modificar():
    form = forms.Alumno(request.form)
    
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
            return redirect(url_for('alumnos.index'))

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
            return redirect(url_for('alumnos.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}')

    return render_template("alumnos/modificar.html", form=form)



@alumnos.route('/alumnos/eliminar', methods=['GET', 'POST'])
def eliminar():
    form = forms.Alumno(request.form)
    
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
            return redirect(url_for('alumnos.index'))

    if request.method == 'POST':
        try:
            id = form.id.data
            alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
            if alumno:
                db.session.delete(alumno)
                db.session.commit()
                flash('Registro eliminado exitosamente')
            return redirect(url_for('alumnos.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al eliminar: {str(e)}')

    return render_template("alumnos/eliminar.html", form=form)