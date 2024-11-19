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
        return redirect(
            url_for(
                "cobros.listar_cobros", success_cobro="Cobro registrado exitosamente."
            )
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

    empleado_alias = aliased(Empleado)

    query = db.session.query(RegistroCobro).join(
        empleado_alias, RegistroCobro.recibido_por == empleado_alias.id
    )

    if fecha_inicio and fecha_fin:
        query = query.filter(RegistroCobro.fecha_pago.between(fecha_inicio, fecha_fin))
    if medio_pago:
        query = query.filter(RegistroCobro.medio_pago == medio_pago.lower())
    if nombre_recibido:
        query = query.filter(empleado_alias.nombre.ilike(f"%{nombre_recibido}%"))
    if apellido_recibido:
        query = query.filter(empleado_alias.apellido.ilike(f"%{apellido_recibido}%"))

    query = query.order_by(
        RegistroCobro.fecha_pago.asc() if orden == "asc" else RegistroCobro.fecha_pago.desc()
    )

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

    if form.validate_on_submit():
        cobro.jinete_id = form.jinete.data
        cobro.fecha_pago = form.fecha_pago.data
        cobro.medio_pago = form.medio_pago.data.lower()
        cobro.monto = form.monto.data
        cobro.recibido_por = form.recibido_por.data
        cobro.observaciones = form.observaciones.data

        cobros.actualizar_cobro()
        return redirect(
            url_for("cobros.listar_cobros", success_cobro="Cobro editado exitosamente.")
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
