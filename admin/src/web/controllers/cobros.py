from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.database import db
from src.core.cobros.models import RegistroCobro
from src.core.cobros.forms import RegistroCobroForm
from src.core.equipo.models import Empleado

cobros_bp = Blueprint("cobros", __name__, template_folder="../templates/cobros")


@cobros_bp.route("/registrar", methods=["GET", "POST"])
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
            estado_pago=form.estado_pago.data,
        )

        db.session.add(nuevo_cobro)
        db.session.commit()
        return redirect(url_for("cobros.listar_cobros"))

    return render_template("registrar_cobro.html", form=form)


@cobros_bp.route("/listado", methods=["GET"])
def listar_cobros():
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    medio_pago = request.args.get("medio_pago")
    nombre_recibido = request.args.get("nombre_recibido")
    apellido_recibido = request.args.get("apellido_recibido")
    orden = request.args.get("orden", "asc")

    query = RegistroCobro.query

    if fecha_inicio and fecha_fin:
        query = query.filter(RegistroCobro.fecha_pago.between(fecha_inicio, fecha_fin))

    if medio_pago:
        query = query.filter(RegistroCobro.medio_pago == medio_pago.lower())

    if nombre_recibido:
        query = query.join(Empleado).filter(
            Empleado.nombre.ilike(f"%{nombre_recibido}%")
        )

    if apellido_recibido:
        query = query.join(Empleado).filter(
            Empleado.apellido.ilike(f"%{apellido_recibido}%")
        )

    if orden == "desc":
        cobros_realizado = query.order_by(RegistroCobro.fecha_pago.desc()).all()
    else:
        cobros_realizado = query.order_by(RegistroCobro.fecha_pago.asc()).all()

    return render_template("listado_cobros.html", cobros_realizado=cobros_realizado)

@cobros_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_cobro(id):
    cobro = RegistroCobro.query.get_or_404(id)
    form = RegistroCobroForm(obj=cobro)

    if form.validate_on_submit():
        cobro.jinete_id = form.jinete.data
        cobro.fecha_pago = form.fecha_pago.data
        cobro.medio_pago = form.medio_pago.data.lower()
        cobro.monto = form.monto.data
        cobro.recibido_por = form.recibido_por.data
        cobro.observaciones = form.observaciones.data
        cobro.estado_pago = form.estado_pago.data

        db.session.commit()
        return redirect(url_for("cobros.listar_cobros"))

    return render_template("editar_cobro.html", form=form, cobro=cobro)


@cobros_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_cobro(id):
    cobro = RegistroCobro.query.get_or_404(id)
    db.session.delete(cobro)
    db.session.commit()
    flash("Cobro eliminado exitosamente.")
    return redirect(url_for("cobros.listar_cobros"))


@cobros_bp.route("/buscar", methods=["GET"])
def buscar_cobros():
    medio_pago = request.args.get("medio_pago")
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    nombre_recibe = request.args.get("nombre_recibe")
    apellido_recibe = request.args.get("apellido_recibe")

    query = RegistroCobro.query

    if medio_pago:
        query = query.filter(RegistroCobro.medio_pago == medio_pago)
    if fecha_inicio and fecha_fin:
        query = query.filter(RegistroCobro.fecha_pago.between(fecha_inicio, fecha_fin))
    if nombre_recibe:
        query = query.filter(RegistroCobro.quien_recibe.has(nombre=nombre_recibe))
    if apellido_recibe:
        query = query.filter(RegistroCobro.quien_recibe.has(apellido=apellido_recibe))

    cobros = query.order_by(RegistroCobro.fecha_pago).all()

    return render_template("listado_cobros.html", cobros=cobros)
