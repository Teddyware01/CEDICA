# src/web/controllers/equipo.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.equipo.models import Empleado, Profesion, PuestoLaboral, CondicionEnum
from src.core.equipo.extra_models import Domicilio, ContactoEmergencia
from src.core.equipo.forms import EmpleadoForm
from src.core import equipo

from src.core.database import db

bp = Blueprint("equipo", __name__, url_prefix="/equipo")


@bp.get("/")
def listar_empleados():
    sort_by = request.args.get("sort_by")

    # usa lo de... src/core/equipo/__init__.py
    empleados = equipo.list_empleados(sort_by=sort_by)
    return render_template("equipo/equipo.html", empleados=empleados)


@bp.get("/agregar_empleado")
def add_client_form():
    return render_template("equipo/add_empleado.html")


@bp.get("/editar_cliente<int:user_id>")
def edit_empleado_form(user_id):
    empleado = equipo.Empleado.query.get(user_id)
    return render_template("equipo/edit_empleado.html", empleado=empleado)


@bp.get("/eliminar_cliente<int:user_id>")
def delete_client_form(user_id):
    empleado = equipo.Empleado.query.get(user_id)
    return render_template("equipo/delete_empleado.html", empleado=empleado)


# probar si esta bien asi o si va "request.form.campo" en lugar de "form.campo"
@bp.post("/agregar_empleado")
def add_empleado():
    form = EmpleadoForm()

    # Cargar las opciones para los campos de selección
    form.profesion_id.choices = [(p.id, p.nombre) for p in equipo.list_profesiones()]
    form.puesto_laboral_id.choices = [
        (p.id, p.nombre) for p in equipo.list_puestos_laborales()
    ]
    form.condicion.choices = [(p.id, p.nombre) for p in CondicionEnum.query.all()]

    if form.validate_on_submit():
        # Crear nuevo Domicilio registrado con los datos del formulario
        # Crear nuevo Contacto de emergencia registrado con los datos del formulario
        nuevo_contacto_emergencia = equipo.create_contacto_emergencia(
            nombre=form.contacto_emergencia_nombre,
            apellido=form.contacto_emergencia_apellido,
            telefono=form.contacto_emergencia_telefono,
        )

        nuevo_domicilio = equipo.create_domicilio(
            calle=form.domicilio_calle,
            numero=form.domicilio_numero,
            departamento=form.domicilio_departamento,
            piso=form.domicilio_piso,
            localidad=form.domicilio_localidad,
            provincia=form.domicilio_provincia,
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
            contacto_emergencia_id=nuevo_contacto_emergencia.id,
            domicilio_id=nuevo_domicilio.id,
        )

        flash("Empleado registrado exitosamente", "success")
        return redirect(url_for("equipo.listar_empleados"))
    else:
        flash("ERRORES::::.", "error")
        return redirect(url_for("equipo.add_empleado"))


@bp.post("/eliminar_empleado<int:empleado_id>")
def delete_empleado(empleado_id):
    equipo.delete_empleado(empleado_id)
    return redirect(url_for("equipo.listar_empleados"))


@bp.post("/editar_empleado<int:empleado_id>")
def update_user(empleado_id):
    # COMPLETAR...
    #
    #
    flash("Empleado actualizado exitosamente", "success")
    return redirect(url_for("equipo.listar_empleados"))
