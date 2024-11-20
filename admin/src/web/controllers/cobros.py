from flask import Blueprint, request, render_template, redirect, url_for, flash
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

    if form.validate_on_submit():
        nuevo_cobro = RegistroCobro(
            jinete_id=form.jinete.data,
            fecha_pago=form.fecha_pago.data,
            medio_pago=form.medio_pago.data,
            monto=form.monto.data,
            recibido_por=form.recibido_por.data,
            observaciones=form.observaciones.data,
        )

        cobros.agregar_cobro(nuevo_cobro)
        return render_template(
            "confirmar_cobro.html",
            cobro=nuevo_cobro,
            form=form,
        )

    return render_template("registrar_cobro.html", form=form)

@cobros_bp.route("/listado", methods=["GET"])
@login_required
@check("cobro_index")
def listar_cobros():
    page = request.args.get("page", 1, type=int)
    per_page = 5

    fecha_inicio = request.args.get("fecha_inicio", "")
    fecha_fin = request.args.get("fecha_fin", "")
    medio_pago = request.args.get("medio_pago", "")
    nombre_recibido = request.args.get("nombre_recibido", "")
    apellido_recibido = request.args.get("apellido_recibido", "")
    orden = request.args.get("orden", "asc")

    empleado_alias = cobros.buscar_empleado()

    query = cobros.buscar_empleado_por_id(empleado_alias)

    query = cobros.operaciones_filtro(fecha_inicio, fecha_fin, medio_pago, nombre_recibido, apellido_recibido, empleado_alias, query)

    query = cobros.ordenar_fecha(orden, query)

    cobros_realizado = query.paginate(page=page, per_page=per_page)

    success_cobro = request.args.get("success_cobro")

    return render_template(
        "listado_cobros.html",
        cobros_realizado=cobros_realizado.items,
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

    if not cobro:
        return redirect(url_for("cobros.listar_cobros"))

    if request.method == "POST" and form.validate_on_submit():
        cobro.jinete_id = form.jinete.data
        cobro.fecha_pago = form.fecha_pago.data
        cobro.medio_pago = form.medio_pago.data.lower()
        cobro.monto = form.monto.data
        cobro.recibido_por = form.recibido_por.data
        cobro.observaciones = form.observaciones.data

        cobros.actualizar_cobro()
        return render_template(
            "confirmar_cobro.html",
            cobro=cobro,
            form=form,
        )

    return render_template("editar_cobro.html", form=form, cobro=cobro)


@cobros_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
@check("cobro_index")
def eliminar_cobro(id):
    cobro = cobros.obtener_cobro(id)
    cobros.eliminar_cobro(cobro)
    return redirect(url_for("cobros.listar_cobros"))


@cobros_bp.route("/buscar", methods=["GET"])
@login_required
@check("cobro_show")
def buscar_cobros():
    page = request.args.get("page", 1, type=int)
    per_page = 5

    medio_pago = request.args.get("medio_pago")
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    nombre_recibe = request.args.get("nombre")
    apellido_recibe = request.args.get("apellido")
    orden = request.args.get("orden", "asc")

    query = cobros.buscar_cobros(
        medio_pago, fecha_inicio, fecha_fin, nombre_recibe, apellido_recibe, orden
    )
    cobros_realizado = cobros.obtener_todos(query).paginate(
        page=page, per_page=per_page
    )

    return render_template(
        "listado_cobros.html",
        cobros_realizado=cobros_realizado.items,
        pagination=cobros_realizado,
    )

@cobros_bp.route("/confirmar_registro", methods=["POST"])
@login_required
@check("cobro_create")
def confirmar_registro_cobro():
    action = request.form.get("action")
    if action == "aceptar":
        cobro_data = request.form
        nuevo_cobro = RegistroCobro(
            jinete_id=cobro_data.get("jinete_id"),
            fecha_pago=cobro_data.get("fecha_pago"),
            medio_pago=cobro_data.get("medio_pago"),
            monto=float(cobro_data.get("monto")),
            recibido_por=cobro_data.get("recibido_por"),
            observaciones=cobro_data.get("observaciones"),
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
        return render_template("registrar_cobro.html", form=form)
    else:
        return redirect(url_for("cobros.listar_cobros"))

@cobros_bp.route("/confirmar_edicion/<int:id>", methods=["POST"])
@login_required
@check("cobro_update")
def confirmar_edicion_cobro(id):
    action = request.form.get("action")
    if action == "aceptar":
        cobro_data = request.form
        cobro = cobros.obtener_cobro(id)
        cobro.jinete_id = cobro_data.get("jinete_id")
        cobro.fecha_pago = cobro_data.get("fecha_pago")
        cobro.medio_pago = cobro_data.get("medio_pago")
        cobro.monto = float(cobro_data.get("monto"))
        cobro.recibido_por = cobro_data.get("recibido_por")
        cobro.observaciones = cobro_data.get("observaciones")
        cobros.actualizar_cobro()
        return redirect(
            url_for("cobros.listar_cobros", success_cobro="Cobro editado exitosamente.")
        )
    elif action == "editar":
        cobro = cobros.obtener_cobro(id)
        form = RegistroCobroForm(
            jinete=cobro.jinete_id,
            fecha_pago=cobro.fecha_pago,
            medio_pago=cobro.medio_pago,
            monto=cobro.monto,
            recibido_por=cobro.recibido_por,
            observaciones=cobro.observaciones,
        )
        return render_template("editar_cobro.html", form=form, cobro=cobro)
    else:
        return redirect(url_for("cobros.listar_cobros"))
