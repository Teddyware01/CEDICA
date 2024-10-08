# src/web/controllers/equipo.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.equipo.models import Empleado, Profesion, PuestoLaboral, CondicionEnum
from src.core.equipo.extra_models import Domicilio, ContactoEmergencia
from src.core.equipo.forms import AddEmpleadoForm
from src.core import equipo

from src.core.database import db

bp = Blueprint("equipo", __name__, url_prefix="/equipo")


@bp.get("/")
def listar_empleados():
    sort_by = request.args.get("sort_by")
    id_puesto_laboral = request.args.get("id_puesto_laboral")
    search = request.args.get("search")

    # usa lo de... src/core/equipo/__init__.py
    empleados = equipo.list_empleados(
        sort_by=sort_by, id_puesto_laboral=id_puesto_laboral, search=search
    )
    puestos_laborales = equipo.list_puestos_laborales()
    return render_template(
        "equipo/equipo.html", empleados=empleados, puestos_laborales=puestos_laborales
    )


@bp.get("/agregar_empleado")
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

    return render_template("equipo/add_empleado.html", form=form)


@bp.get("/ver_empleado<int:empleado_id>")
def show_empleado(empleado_id):
    empleado = equipo.Empleado.query.get(empleado_id)

    # Luego se cargaran los documentos adjuntos.
    documentos = None
    return render_template(
        "equipo/show_empleado.html", empleado=empleado, documentos=documentos
    )


@bp.post("/eliminar_empleado/<int:empleado_id>")
def delete_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    try:
        equipo.delete_empleado(empleado_id)
        flash("Empleado eliminado exitosamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar el empleado: {str(e)}", "danger")

    return redirect(url_for("equipo.listar_empleados"))


# probar si esta bien asi o si va "request.form.campo" en lugar de "form.campo"
@bp.post("/agregar_empleado")
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
        flash("Por favor corrija los errores en el formulario:", "error")
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    f"Error en el campo {getattr(form, field).label.text}: {error}",
                    "danger",
                )

        return redirect(url_for("equipo.add_empleado_form"))


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


@bp.get("/editar_empleado<int:empleado_id>")
def edit_empleado_form(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)  # Obtener el empleado
    form = AddEmpleadoForm(
        obj=empleado
    )  # Poblar el formulario con los datos del empleado

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
        )  # Asegúrate de que `localidad` es el ID
        empleado.domicilio.provincia_id = (
            form.domicilio_provincia.data
        )  # Asegúrate de que `provincia` es el ID

        # Asignar los valores del contacto de emergencia
        empleado.contacto_emergencia.nombre = form.contacto_emergencia_nombre.data
        empleado.contacto_emergencia.apellido = form.contacto_emergencia_apellido.data
        empleado.contacto_emergencia.telefono = form.contacto_emergencia_telefono.data

        # Guardar los cambios en la base de datos
        flash("Empleado registrado  exitosamente", "success")
        db.session.commit()
        return show_empleado(empleado_id=empleado.id)
    else:
        flash("Por favor corrija los errores en el formulario:", "error")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en el campo {field}: {error}", "danger")

    return render_template("equipo/edit_empleado.html", form=form, empleado=empleado)
