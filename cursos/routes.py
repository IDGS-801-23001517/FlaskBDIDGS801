from . import cursos
from flask import render_template, request, redirect, url_for, flash
from models import db, Curso, Maestros, Alumnos
import forms

@cursos.route("/cursos")
def index():
    try:
        lista_cursos = Curso.query.all()
    except Exception as e:
        print(f"Error BD: {e}")
        lista_cursos = []
    return render_template("cursos/cursos.html", cursos=lista_cursos)

@cursos.route("/cursos/detalles", methods=['GET'])
def detalles():
    id = request.args.get('id')
    curso = db.session.query(Curso).filter(Curso.id == id).first()
    if curso:
        return render_template("cursos/detalles.html", curso=curso)
    flash('Curso no encontrado')
    return redirect(url_for('cursos.index'))

@cursos.route("/cursos/agregar", methods=['GET', 'POST'])
def agregar():
    form = forms.Curso(request.form)
    form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()]
    
    if request.method == 'POST' and form.validate():
        try:
            curso = Curso(
                nombre=form.nombre.data,
                descripcion=form.descripcion.data,
                maestro_id=form.maestro_id.data
            )
            db.session.add(curso)
            db.session.commit()
            flash('Curso registrado correctamente')
            return redirect(url_for('cursos.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar: {str(e)}')
    return render_template("cursos/agregar.html", form=form)

@cursos.route("/cursos/modificar", methods=['GET', 'POST'])
def modificar():
    form = forms.Curso(request.form)
    form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()]
    
    if request.method == 'GET':
        id = request.args.get('id')
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        if curso:
            form.id.data = curso.id
            form.nombre.data = curso.nombre
            form.descripcion.data = curso.descripcion
            form.maestro_id.data = curso.maestro_id
        else:
            flash('Curso no encontrado')
            return redirect(url_for('cursos.index'))

    if request.method == 'POST' and form.validate():
        try:
            id = form.id.data
            curso = db.session.query(Curso).filter(Curso.id == id).first()
            if curso:
                curso.nombre = form.nombre.data
                curso.descripcion = form.descripcion.data
                curso.maestro_id = form.maestro_id.data
                db.session.commit()
                flash('Curso actualizado correctamente')
            return redirect(url_for('cursos.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}')
    return render_template("cursos/modificar.html", form=form)

@cursos.route('/cursos/eliminar', methods=['GET', 'POST'])
def eliminar():
    form = forms.Curso(request.form)
    form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()]
    
    if request.method == 'GET':
        id = request.args.get('id')
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        if curso:
            form.id.data = curso.id
            form.nombre.data = curso.nombre
            form.descripcion.data = curso.descripcion
            form.maestro_id.data = curso.maestro_id
        else:
            flash('Curso no existe')
            return redirect(url_for('cursos.index'))

    if request.method == 'POST':
        try:
            id = form.id.data
            curso = db.session.query(Curso).filter(Curso.id == id).first()
            if curso:
                db.session.delete(curso)
                db.session.commit()
                flash('Registro eliminado exitosamente')
            return redirect(url_for('cursos.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al eliminar: {str(e)}')
    return render_template("cursos/eliminar.html", form=form)

@cursos.route("/cursos/inscribir", methods=['GET', 'POST'])
def inscribir():
    form = forms.Inscripcion(request.form)
    form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in Alumnos.query.all()]
    form.curso_id.choices = [(c.id, c.nombre) for c in Curso.query.all()]
    
    if request.method == 'POST' and form.validate():
        try:
            curso = Curso.query.get(form.curso_id.data)
            alumno = Alumnos.query.get(form.alumno_id.data)
            if curso and alumno:
                if alumno not in curso.alumnos:
                    curso.alumnos.append(alumno)
                    db.session.commit()
                    flash('Alumno inscrito correctamente')
                else:
                    flash('El alumno ya está inscrito en este curso')
            return redirect(url_for('cursos.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al inscribir: {str(e)}')
    
    curso_id = request.args.get('curso_id')
    if request.method == 'GET' and curso_id:
        form.curso_id.data = int(curso_id)

    return render_template("cursos/inscribir.html", form=form)