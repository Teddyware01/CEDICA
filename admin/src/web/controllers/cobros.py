from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from src.core.jya.models import Jinete
from src.core.database import db
from src.core.cobros.models import RegistroCobro
from src.core.cobros.forms import RegistroCobroForm
from src.core.equipo.models import Empleado
from src.core import cobros
from src.web.handlers.auth import login_required, check
from sqlalchemy.orm import aliased

cobros_bp = Blueprint("cobros", __name__, template_folder="../templates/cobros")

@cobros_bp.route("/registrar", methods=["GET", "POST"])
@login_required
@check("cobro_create")
def registrar_cobro():
    form = RegistroCobroForm()

    jinetes_activados = Jinete.query.filter_by(esta_borrado=False).all()
    empleados_disponibles = Empleado.query.filter_by(esta_borrado=False).all()

    if not jinetes_activados:
        flash("No hay jinetes o amazonas disponibles para registrar el cobro.", "danger")
        return redirect(url_for("cobros.listar_cobros"))

    if not empleados_disponibles:
        flash("No hay empleados disponibles para registrar el cobro.", "danger")
        return redirect(url_for("cobros.listar_cobros"))

    if form.validate_on_submit():
        jinete_id = request.form.get("jinete")
        recibido_por = request.form.get("recibido_por")

        jinete = cobros.obtener_jinete(jinete_id)
        empleado = cobros.obtener_empleado(recibido_por)


        nombre_jinete = jinete.nombre
        apellido_jinete = jinete.apellido

        nuevo_cobro = RegistroCobro(
            jinete_id=jinete_id,
            fecha_pago=request.form.get("fecha_pago"),
            medio_pago=request.form.get("medio_pago"),
            monto=float(request.form.get("monto")),
            recibido_por=recibido_por,
            observaciones=request.form.get("observaciones"),
        )

        """ Renderizar la vista de confirmación con los valores correctos, tengo que pasar
        el nombre_jinete y apellido_jinete para la visualizacion en la pantalla de confirmacion
        """
        return render_template(
            "confirmar_cobro.html",
            cobro=nuevo_cobro,
            jinete=jinete,
            empleado=empleado,
            nombre_jinete=nombre_jinete,
            apellido_jinete=apellido_jinete
        )

    return render_template("registrar_cobro.html", form=form, jinetes_activados=jinetes_activados, empleados_disponibles=empleados_disponibles)

@cobros_bp.route("/listado", methods=["GET"], endpoint="cobros_listado")
@login_required
@check("cobro_index")
def listar_cobros():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("PAGINATION_PER_PAGE")

    fecha_inicio = request.args.get("fecha_inicio", "")
    fecha_fin = request.args.get("fecha_fin", "")
    medio_pago = request.args.get("medio_pago", "")
    nombre_recibido = request.args.get("nombre_recibido", "")
    apellido_recibido = request.args.get("apellido_recibido", "")
    orden = request.args.get("orden", "asc")

    empleado_alias = cobros.buscar_empleado()
    query = cobros.buscar_empleado_por_id(empleado_alias)
    query = cobros.operaciones_filtro(
        fecha_inicio, fecha_fin, medio_pago, nombre_recibido, apellido_recibido, empleado_alias, query
    )
    query = cobros.ordenar_fecha(orden, query)

    cobros_realizado = query.paginate(page=page, per_page=per_page)

    success_cobro = request.args.get("success_cobro")

    return render_template(
        "listado_cobros.html",
        cobros_realizado=cobros_realizado.items,
        pagina_actual=cobros_realizado.page,
        total_paginas=cobros_realizado.pages,
        pagination=cobros_realizado,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        medio_pago=medio_pago,
        nombre_recibido=nombre_recibido,
        apellido_recibido=apellido_recibido,
        orden=orden,
        success_cobro=success_cobro,
    )


@cobros_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
@check("cobro_update")
def editar_cobro(id):
    cobro = cobros.obtener_cobro(id)
    form = cobros.obtener_cobro_param(cobro)

    jinetes_activados = Jinete.query.filter_by(esta_borrado=False).all()

    empleados_disponibles = Empleado.query.filter_by(esta_borrado=False).all()

    if request.method == "POST" and form.validate_on_submit() and (jinetes_activados and empleados_disponibles):
        cobro.jinete_id = form.jinete.data
        cobro.fecha_pago = form.fecha_pago.data
        cobro.medio_pago = form.medio_pago.data.lower()
        cobro.monto = form.monto.data
        cobro.recibido_por = form.recibido_por.data
        cobro.observaciones = form.observaciones.data

        jinete = cobros.obtener_jinete(form.jinete.data)
        empleado = cobros.obtener_empleado(form.recibido_por.data)

        nombre_jinete = jinete.nombre
        apellido_jinete = jinete.apellido

        db.session.commit()
        return redirect(url_for('cobros.listar_cobros'))
    else:
        if not jinetes_activados:
            flash("No hay jinetes o amazonas disponibles para editar el cobro.", "danger")
            return redirect(url_for("cobros.listar_cobros"))

        if not empleados_disponibles:
            flash("No hay empleados disponibles para registrar el cobro.", "danger")
            return redirect(url_for("cobros.listar_cobros"))

    return render_template("editar_cobro.html", form=form, cobro=cobro, jinetes_activados=jinetes_activados, empleados_disponibles=empleados_disponibles)


@cobros_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
@check("cobro_index")
def eliminar_cobro(id):
    cobro = cobros.obtener_cobro(id)
    cobros.eliminar_cobro(cobro)
    return redirect(url_for("cobros.listar_cobros"))


@cobros_bp.route("/listado", methods=["GET"])
@login_required
@check("cobro_index")
def listar_cobros():
    # Obtener parámetros de entrada con valores predeterminados
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("PAGINATION_PER_PAGE", 3)

    fecha_inicio = request.args.get("fecha_inicio", "")
    fecha_fin = request.args.get("fecha_fin", "")
    medio_pago = request.args.get("medio_pago", "")
    nombre_recibido = request.args.get("nombre_recibido", "")
    apellido_recibido = request.args.get("apellido_recibido", "")
    orden = request.args.get("orden", "asc")
    success_cobro = request.args.get("success_cobro")
    empleado_alias = cobros.buscar_empleado()
    query = cobros.buscar_empleado_por_id(empleado_alias)
    query = cobros.operaciones_filtro(
        fecha_inicio,
        fecha_fin,
        medio_pago,
        nombre_recibido,
        apellido_recibido,
        empleado_alias,
        query,
    )
    query = cobros.ordenar_fecha(orden, query)
    cobros_realizado = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "listado_cobros.html",
        cobros_realizado=cobros_realizado.items,
        pagination=cobros_realizado,
        pagina_actual=cobros_realizado.page,
        total_paginas=cobros_realizado.pages,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        medio_pago=medio_pago,
        nombre_recibido=nombre_recibido,
        apellido_recibido=apellido_recibido,
        orden=orden,
        success_cobro=success_cobro,
    )


@cobros_bp.route("/confirmar_registro", methods=["POST"])
@login_required
@check("cobro_create")
def confirmar_registro_cobro():
    action = request.form.get("action")
    jinete_id = request.form.get("jinete_id")
    if action == "aceptar":
        nuevo_cobro = RegistroCobro(
            jinete_id=jinete_id,
            fecha_pago=request.form.get("fecha_pago"),
            medio_pago=request.form.get("medio_pago"),
            monto=float(request.form.get("monto")),
            recibido_por=request.form.get("recibido_por"),
            observaciones=request.form.get("observaciones"),
        )
        cobros.agregar_cobro(nuevo_cobro)
        return redirect(
            url_for("cobros.listar_cobros", success_cobro="Cobro registrado exitosamente.")
        )
    elif action == "editar":
        form = RegistroCobroForm(
            jinete=request.form.get("jinete_id"),
            fecha_pago=request.form.get("fecha_pago"),
            medio_pago=request.form.get("medio_pago"),
            monto=request.form.get("monto"),
            recibido_por=request.form.get("recibido_por"),
            observaciones=request.form.get("observaciones"),
        )
        # Recuperar los datos de jinetes y empleados
        jinetes_activados = Jinete.query.filter_by(esta_borrado=False).all()
        empleados_disponibles = Empleado.query.filter_by(esta_borrado=False).all()

        return render_template(
            "registrar_cobro.html",
            form=form,
            jinetes_activados=jinetes_activados,
            empleados_disponibles=empleados_disponibles
        )
    elif action == "cancelar":
        return redirect(url_for("cobros.listar_cobros"))

@cobros_bp.route("/confirmar_eliminar/<int:id>", methods=["GET", "POST"])
@login_required
@check("cobro_delete")
def confirmar_eliminar_cobro(id):
    cobro = cobros.obtener_cobro(id)
    jinete = cobros.obtener_jinete(cobro.jinete_id)
    empleado = cobros.obtener_empleado(cobro.recibido_por)

    if request.method == "POST":
        action = request.form.get("action")

        if action == "aceptar":
            # Eliminar el cobro
            cobros.eliminar_cobro(cobro)
            flash("Cobro eliminado exitosamente.", "success")
            return redirect(url_for("cobros.listar_cobros"))
        elif action == "rechazar":
            flash("Eliminación del cobro cancelada.", "info")
            return redirect(url_for("cobros.listar_cobros"))

    return render_template(
        "confirmar_eliminar_cobro.html",
        cobro=cobro,
        jinete=jinete,
        empleado=empleado
    )
