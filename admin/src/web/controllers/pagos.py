from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.database import db
from src.core.pagos.models import Pago as Pagos
from src.core.pagos.forms import PagoForm

# Crear el Blueprint
pagos_bp = Blueprint("pagos", __name__, template_folder="../templates/pagos")

# Endpoint para registrar un nuevo pago
@pagos_bp.route("/registrar", methods=["GET", "POST"])
def registrar_pago():
    form = PagoForm()
    if form.validate_on_submit():
        nuevo_pago = Pagos(
            beneficiario=form.beneficiario.data,
            monto=form.monto.data,
            fecha_pago=form.fecha_pago.data,
            tipo_pago=form.tipo_pago.data,
            descripcion=form.descripcion.data,
        )
        db.session.add(nuevo_pago)
        db.session.commit()
        flash("Pago registrado exitosamente.")
        return redirect(url_for("pagos.listar_pagos"))  # Redirigir al listado de pagos

    return render_template("registrar_pago.html", form=form)  # Mostrar formulario

# Endpoint para listar todos los pagos
@pagos_bp.route("/listado", methods=["GET"])
def listar_pagos():
    pagos_realizado = Pagos.query.all()  # Obtener todos los pagos
    return render_template("listado_pagos.html", pagos_realizado=pagos_realizado)  # Renderizar la lista de pagos

# Endpoint para mostrar un pago específico
@pagos_bp.route("/<int:id>", methods=["GET"])
def mostrar_pagos(id):
    pago = Pagos.query.get_or_404(id)  # Obtener el pago por ID
    return render_template("show_pago.html", pago=pago)  # Mostrar detalle del pago


@pagos_bp.route("/search", methods=["GET"])
def buscar_pagos():
    tipo_pago = request.args.get("tipo_pago")
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    orden = request.args.get("orden", "asc")  # Obtener el orden, por defecto ascendente
    
    query = Pagos.query

    # Filtrar por tipo de pago
    if tipo_pago:
        query = query.filter(Pagos.tipo_pago == tipo_pago)
    
    # Filtrar por rango de fechas
    if fecha_inicio and fecha_fin:
        query = query.filter(Pagos.fecha_pago.between(fecha_inicio, fecha_fin))
    
    # Ordenar resultados
    if orden == "desc":
        pagos = query.order_by(Pagos.fecha_pago.desc()).all()  # Orden descendente
    else:
        pagos = query.order_by(Pagos.fecha_pago).all()  # Orden ascendente

    return render_template("listado_pagos.html", pagos_realizado=pagos)  # Mostrar resultados de búsqueda