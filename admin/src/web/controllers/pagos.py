from flask import Blueprint, request, render_template, redirect, url_for, flash 
from src.core.database import db
from src.core.pagos.models import Pago as Pagos
from src.core.equipo.models import Empleado
from src.core.pagos.forms import PagoForm
from src.web.handlers.auth import login_required, check

pagos_bp = Blueprint("pagos", __name__, template_folder="../templates/pagos")

@pagos_bp.route("/registrar", methods=["GET", "POST"])
@login_required
@check("pago_create")
def registrar_pago():
    form = PagoForm()

    if form.validate_on_submit():
        if form.tipo_pago.data == 'honorario' and form.beneficiario.data:
            empleado = Empleado.query.get(form.beneficiario.data)
            beneficiario = f"{empleado.nombre} {empleado.apellido}"
        else:
            beneficiario = form.otro_beneficiario.data

        nuevo_pago = Pagos(
            beneficiario=beneficiario,
            monto=form.monto.data,
            fecha_pago=form.fecha_pago.data,
            tipo_pago=form.tipo_pago.data.lower(),
            descripcion=form.descripcion.data,
        )

        db.session.add(nuevo_pago)
        db.session.commit()

        #flash("Pago registrado exitosamente.", "success")
        return redirect(url_for("pagos.listar_pagos"))

    return render_template("registrar_pago.html", form=form)

@pagos_bp.route("/listado", methods=["GET"])
@login_required
@check("pago_index")
def listar_pagos():
    orden = request.args.get("orden", "asc")
    pagos_realizado = Pagos.query.order_by(Pagos.fecha_pago.asc() if orden == "asc" else Pagos.fecha_pago.desc()).all()
    return render_template("listado_pagos.html", pagos_realizado=pagos_realizado, orden=orden)

@pagos_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
@check("pago_destroy")
def eliminar_pago(id):
    pago = Pagos.query.get_or_404(id)
    db.session.delete(pago)
    db.session.commit()
    ##flash("Pago eliminado exitosamente.")
    return redirect(url_for("pagos.listar_pagos"))

@pagos_bp.route("/<int:id>", methods=["GET"])
@login_required
@check("pago_show")
def mostrar_pagos(id):
    pago = Pagos.query.get_or_404(id)
    return render_template("show_pago.html", pago=pago)

@pagos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
@check("pago_update")
def editar_pago(id):
    pago = Pagos.query.get_or_404(id)
    
    if pago.tipo_pago != 'honorario':
        form = PagoForm(obj=pago, otro_beneficiario=pago.beneficiario)
    else:
        form = PagoForm(obj=pago)

    if form.validate_on_submit():
        if form.tipo_pago.data == 'honorario':
            if form.beneficiario.data:
                empleado = Empleado.query.get(form.beneficiario.data)
                pago.beneficiario = f"{empleado.nombre} {empleado.apellido}"
        else:
            pago.beneficiario = form.otro_beneficiario.data

        pago.monto = form.monto.data
        pago.fecha_pago = form.fecha_pago.data
        pago.tipo_pago = form.tipo_pago.data.lower()
        pago.descripcion = form.descripcion.data

        db.session.commit()
        #flash("Pago actualizado exitosamente.", "success")
        return redirect(url_for("pagos.listar_pagos"))

    return render_template("editar_pago.html", form=form, pago=pago)

@pagos_bp.route("/search", methods=["GET"])
@login_required
@check("pago_index") ## aca tener cuiddado si revienta puede ser esto
def buscar_pagos():
    tipo_pago = request.args.get("tipo_pago").lower() if request.args.get("tipo_pago") else None
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    orden = request.args.get("orden", "asc")
    
    query = Pagos.query
    if tipo_pago:
        query = query.filter(db.func.lower(Pagos.tipo_pago) == tipo_pago)
    if fecha_inicio and fecha_fin:
        query = query.filter(Pagos.fecha_pago.between(fecha_inicio, fecha_fin))
    if orden == "desc":
        pagos = query.order_by(Pagos.fecha_pago.desc()).all()
    else:
        pagos = query.order_by(Pagos.fecha_pago).all()

    return render_template("listado_pagos.html", pagos_realizado=pagos)