from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.database import db
from src.core.pagos.models import Pago as pagos

# Crear el Blueprint
pagos_bp = Blueprint("pagos", __name__, template_folder="../templates/pagos")


@pagos_bp.route("/", methods=["GET", "POST"])
def registrar_pago():
    if request.method == "POST":
        beneficiario = request.form["beneficiario"]
        monto = request.form["monto"]
        fecha_pago = request.form["fecha_pago"]
        tipo_pago = request.form["tipo_pago"]
        descripcion = request.form["descripcion"]

        nuevo_pago = pagos(
            beneficiario=beneficiario,
            monto=monto,
            fecha_pago=fecha_pago,
            tipo_pago=tipo_pago,
            descripcion=descripcion,
        )
        db.session.add(nuevo_pago)
        db.session.commit()
        flash("Pago registrado exitosamente.")

        return redirect(url_for("pagos.index"))

    pagos_realizado = pagos.query.all()
    return render_template("home.html", pagos_realizado=pagos)


@pagos_bp.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
def mostrar_pago(id):
    pagos_realizado = pagos.query.get_or_404(id)
    if request.method == "PUT":
        # Lógica para actualizar el pago
        pass
    elif request.method == "DELETE":
        db.session.delete(pagos_realizado)
        db.session.commit()
        flash("Pago eliminado exitosamente.")
        return redirect(url_for("pagos.index"))
    return render_template("show.html", pagos_realizado=pagos_realizado)


@pagos_bp.route("/search", methods=["GET"])
def buscar_pago():
    tipo_pago = request.args.get("tipo_pago")
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    
    query = pagos.query

    if tipo_pago:
        query = query.filter(pagos.tipo_pago == tipo_pago)
    if fecha_inicio and fecha_fin:
        query = query.filter(pagos.fecha_pago.between(fecha_inicio, fecha_fin))

    pagos = query.order_by(pagos.fecha_pago).all()
    return render_template("home.html", pagos=pagos)