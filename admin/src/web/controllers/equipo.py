# src/web/controllers/equipo.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import session
from src.core.equipo.models import Empleado, Profesion, PuestoLaboral, CondicionEnum
from src.core.equipo.extra_models import Domicilio, ContactoEmergencia
from src.core.equipo.forms import AddEmpleadoForm
from src.core import equipo
from src.core import auth


from flask import current_app
from os import fstat
import re

from src.web.handlers.auth import check,login_required

from src.core.database import db

bp = Blueprint("equipo", __name__, url_prefix="/equipo")


@bp.get("/")
@login_required
@check("empleado_index")
def listar_empleados():
    sort_by = request.args.get("sort_by")
    id_puesto_laboral = request.args.get("id_puesto_laboral")
    search = request.args.get("search")
    page = request.args.get("page", type=int, default=1) 
    # usa lo de... src/core/equipo/__init__.py
    empleados = equipo.list_empleados(
        sort_by=sort_by, id_puesto_laboral=id_puesto_laboral, search=search, page=page
    )
    puestos_laborales = equipo.list_puestos_laborales()
    return render_template(
        "equipo/equipo.html", empleados=empleados, puestos_laborales=puestos_laborales
    )

@bp.get("/agregar_empleado")
@login_required
@check("empleado_create")
def add_empleado_form():

    form = AddEmpleadoForm()

    # Cargar las opciones para los campos de selección
    form.activo.data = True
    form.profesion_id.choices = [(p.id, p.nombre) for p in equipo.list_profesiones()]
    form.domicilio_provincia.choices = [
        (p.id, p.nombre) for p in equipo.list_provincias()
    ]
    # esta linea debe luego reemplazarse por algo dinamico en el html para cargar las opciones tras seleccionar provincia
    form.domicilio_localidad.choices = [
        (p.id, p.nombre) for p in equipo.list_localidades()
    ]
    form.profesion_id.choices = [(p.id, p.nombre) for p in equipo.list_profesiones()]
    form.puesto_laboral_id.choices = [
        (p.id, p.nombre) for p in equipo.list_puestos_laborales()
    ]
    form.condicion.choices = [(e.name, e.value) for e in CondicionEnum]

    return render_template("equipo/agregar_empleado.html", form=form)


@bp.get("/ver_empleado/<int:empleado_id>")
@login_required
@check("empleado_show")
def show_empleado(empleado_id):
    empleado = equipo.Empleado.query.get(empleado_id)
    page = request.args.get('page', 1, type=int)
    documentos_paginated = equipo.traerdocumentos(empleado_id, page=page)
    active_tab = request.args.get('tab', 'general')

    return render_template(
        "equipo/ver_empleado.html", empleado=empleado, documentos_paginated=documentos_paginated,active_tab=active_tab
    )


@bp.get("/eliminar_empleado/<int:empleado_id>")
@login_required
@check("empleado_destroy")
def delete_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    return render_template("equipo/delete_empleado.html", empleado=empleado)

@bp.post("/eliminar_empleado/<int:empleado_id>")
@login_required
@check("empleado_destroy")
def destroy_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    try:
        equipo.delete_empleado(empleado_id)
        flash("Empleado eliminado exitosamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar el empleado: {str(e)}", "danger")

    return redirect(url_for("equipo.listar_empleados"))


@bp.post("/agregar_empleado")
@login_required
@check("empleado_create")
def add_empleado():

    form = AddEmpleadoForm(request.form)
    cargar_choices_form(form)
    if form.validate_on_submit():
        # Crear nuevo Domicilio registrado con los datos del formulario
        localidad = equipo.get_localidad_by_id(form.domicilio_localidad.data)
        provincia = equipo.get_provincia_by_id(form.domicilio_provincia.data)
        nuevo_domicilio = equipo.add_domiclio(
            calle=form.domicilio_calle.data,
            numero=form.domicilio_numero.data,
            departamento=form.domicilio_departamento.data,
            piso=form.domicilio_piso.data,
            localidad=localidad,
            provincia=provincia,
        )
        # Crear nuevo Contacto de emergencia registrado con los datos del formulario
        nuevo_contacto_emergencia = equipo.add_contacto_emergencia(
            nombre=form.contacto_emergencia_nombre.data,
            apellido=form.contacto_emergencia_apellido.data,
            telefono=form.contacto_emergencia_telefono.data,
        )
        # Crear nuevo empleado con los datos del formulario
        equipo.create_empleado(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            dni=form.dni.data,
            email=form.email.data,
            telefono=form.telefono.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_cese=form.fecha_cese.data,
            condicion=form.condicion.data,
            activo=form.activo.data,
            profesion_id=form.profesion_id.data,
            puesto_laboral_id=form.puesto_laboral_id.data,
            obra_social=form.obra_social.data,
            nro_afiliado=form.nro_afiliado.data,
            contacto_emergencia_id=nuevo_contacto_emergencia.id,
            domicilio=nuevo_domicilio,
        )

        flash("Empleado registrado exitosamente", "success")
        return redirect(url_for("equipo.listar_empleados"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    f"Error en el campo {getattr(form, field).label.text}: {error}",
                    "danger",
                )

        return redirect(url_for("equipo.agregar_empleado"))


def cargar_choices_form(form, empleado=None):
    # Cargar las opciones para los campos de selección
    form.profesion_id.choices = [(p.id, p.nombre) for p in equipo.list_profesiones()]
    form.puesto_laboral_id.choices = [
        (p.id, p.nombre) for p in equipo.list_puestos_laborales()
    ]
    form.domicilio_provincia.choices = [
        (p.id, p.nombre) for p in equipo.list_provincias()
    ]
    form.domicilio_localidad.choices = [
        (l.id, l.nombre) for l in equipo.list_localidades()
    ]
    form.condicion.choices = [(e.name, e.value) for e in CondicionEnum]


@bp.get("/editar_empleado/<int:empleado_id>")
@login_required
@check("empleado_update")
def edit_empleado_form(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)  # Obtener el empleado
    form = AddEmpleadoForm(
        obj=empleado
    ) 

    cargar_choices_form(form)
    # Asignar los valores del domicilio
    form.domicilio_calle.data = empleado.domicilio.calle
    form.domicilio_numero.data = empleado.domicilio.numero
    form.domicilio_piso.data = empleado.domicilio.piso
    form.domicilio_departamento.data = empleado.domicilio.departamento
    form.domicilio_localidad.data = empleado.domicilio.localidad
    form.domicilio_provincia.data = empleado.domicilio.provincia

    # Asignar los valores del contacto de emergencia
    form.contacto_emergencia_nombre.data = empleado.contacto_emergencia.nombre
    form.contacto_emergencia_apellido.data = empleado.contacto_emergencia.apellido
    form.contacto_emergencia_telefono.data = empleado.contacto_emergencia.telefono

    if form.validate_on_submit():
        form.populate_obj(empleado)
    return render_template("equipo/edit_empleado.html", form=form, empleado=empleado)


@bp.post("/editar_empleado/<int:empleado_id>")
@login_required
@check("empleado_update")
def update_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)  # Obtener el empleado
    form = AddEmpleadoForm(
        obj=empleado
    )  # Poblar el formulario con los datos del empleado
    # Cargar las opciones para los campos de selección
    form.profesion_id.choices = [(p.id, p.nombre) for p in equipo.list_profesiones()]
    form.puesto_laboral_id.choices = [
        (p.id, p.nombre) for p in equipo.list_puestos_laborales()
    ]
    form.domicilio_provincia.choices = [
        (p.id, p.nombre) for p in equipo.list_provincias()
    ]
    form.domicilio_localidad.choices = [
        (l.id, l.nombre) for l in equipo.list_localidades()
    ]
    form.condicion.choices = [(e.name, e.value) for e in CondicionEnum]

    if form.validate_on_submit():
        # Actualizar los datos del empleado con los valores del formulario
        form.populate_obj(empleado)

        # Asignar los valores del domicilio
        empleado.domicilio.calle = form.domicilio_calle.data
        empleado.domicilio.numero = form.domicilio_numero.data
        empleado.domicilio.piso = form.domicilio_piso.data
        empleado.domicilio.departamento = form.domicilio_departamento.data
        empleado.domicilio.localidad_id = (
            form.domicilio_localidad.data
        )
        empleado.domicilio.provincia_id = (
            form.domicilio_provincia.data
        )
        # Asignar los valores del contacto de emergencia
        empleado.contacto_emergencia.nombre = form.contacto_emergencia_nombre.data
        empleado.contacto_emergencia.apellido = form.contacto_emergencia_apellido.data
        empleado.contacto_emergencia.telefono = form.contacto_emergencia_telefono.data

        # Guardar los cambios en la base de datos
        flash("Empleado registrado  exitosamente", "success")
        db.session.commit()
        return redirect(url_for("equipo.show_empleado", empleado_id=empleado.id))

    else:
        flash("Por favor corrija los errores en el formulario:", "error")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en el campo {field}: {error}", "danger")
        return render_template("equipo/edit_empleado.html", form=form, empleado=empleado)


# DOCUMENTOS:


@bp.get("/editar_empleado/<int:empleado_id>/documentos")
def subir_archivo_form(empleado_id):    
    empleado = equipo.Empleado.query.get_or_404(empleado_id)
    return render_template("equipo/add_documento.html", empleado=empleado)



@bp.post("/editar_empleado/<int:empleado_id>/documentos/")
def agregar_documento(empleado_id):

    params = request.form.copy()
    
    if "documento" not in request.files or request.files["documento"].filename == "":
        flash("El archivo es obligatorio.", "error")  # Mensaje de error
        return redirect(url_for("equipo.subir_archivo_form", empleado_id=empleado_id))

    if "documento" in request.files:
        file = request.files["documento"]
        client = current_app.storage.client
        size = fstat(file.fileno()).st_size
        client.put_object("grupo15", file.filename, file, size, content_type=file.content_type)
        equipo.crear_documento(
            titulo=file.filename,
            tipo=request.form["tipo_archivo"], 
            empleado_id=empleado_id
        ) 
    return redirect(url_for("equipo.show_empleado", empleado_id=empleado_id))


@bp.get("/editar_empleado/<int:empleado_id>/documentos/<string:file_name>")
def descargar_archivo(empleado_id, file_name):
    client = current_app.storage.client
    url = client.presigned_get_object("grupo15", file_name, ExpiresIn=10800)  # 3 horas en segundos
    return redirect(url)

@bp.get("/editar_empleado/<int:empleado_id>/documentos/<int:documento_id>/eliminar")
def eliminar_documento_form(empleado_id, documento_id):
    empleado = equipo.Empleado.query.get_or_404(empleado_id)
    documento = equipo.traerdocumentoporid(documento_id)
    return render_template("equipo/delete_documento.html", empleado=empleado, doc=documento)
                    
                    
@bp.post("/editar_empleado/<int:empleado_id>/documentos/<int:documento_id>/eliminar")
def eliminar_documento(empleado_id, documento_id):
    equipo.delete_documento(documento_id)
    return redirect(url_for("equipo.show_empleado", empleado_id=empleado_id, tab='documentos'))