from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.database import db
from src.core.pagos.models import Pago as Pagos
from src.core.equipo.models import Empleado
from src.core.pagos.forms import PagoForm
from src.core import pagos
from src.web.handlers.auth import login_required, check

pagos_bp = Blueprint("pagos", __name__, template_folder="../templates/pagos")

PAGOS_POR_PAGINA = 5


@pagos_bp.route("/registrar", methods=["GET", "POST"])
@login_required
@check("pago_create")
def registrar_pago():
    form = PagoForm()

    if form.validate_on_submit():
        if form.tipo_pago.data == "honorario" and form.beneficiario.data:
            empleado = pagos.obtener_empleado(form)
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

        pagos.agregar_empleado(nuevo_pago)

        return redirect(
            url_for("pagos.listar_pagos", success="Pago registrado exitosamente.")
        )

    return render_template("registrar_pago.html", form=form)


@pagos_bp.route("/listado", methods=["GET"])
@login_required
@check("pago_index")
def listar_pagos():
    orden = request.args.get("orden", "asc")
    page = request.args.get(
        "page", 1, type=int
    )  
    success = request.args.get("success")

    pagos_realizado = pagos.ordenar_pagos(orden)
    total_paginas = (
        len(pagos_realizado) + PAGOS_POR_PAGINA - 1
    ) // PAGOS_POR_PAGINA 
    pagos_pag = pagos_realizado[
        (page - 1) * PAGOS_POR_PAGINA : page * PAGOS_POR_PAGINA
    ]  

    return render_template(
        "listado_pagos.html",
        pagos_realizado=pagos_pag,
        orden=orden,
        success=success,
        total_paginas=total_paginas,
        pagina_actual=page,
    )


@pagos_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
@check("pago_destroy")
def eliminar_pago(id):
    pago = pagos.obtener_pago(id)
    pagos.eliminar_pago(pago)
    return redirect(url_for("pagos.listar_pagos"))


@pagos_bp.route("/<int:id>", methods=["GET"])
@login_required
@check("pago_show")
def mostrar_pagos(id):
    pago = pagos.obtener_pago(id)
    return render_template("show_pago.html", pago=pago)


@pagos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
@check("pago_update")
def editar_pago(id):
    pago = pagos.obtener_pago(id)

    if pago.tipo_pago != "honorario":
        form = PagoForm(obj=pago, otro_beneficiario=pago.beneficiario)
    else:
        form = PagoForm(obj=pago)

    if form.validate_on_submit():
        if form.tipo_pago.data == "honorario":
            if form.beneficiario.data:
                empleado = pagos.obtener_empleado(form)
                pago.beneficiario = f"{empleado.nombre} {empleado.apellido}"
        else:
            pago.beneficiario = form.otro_beneficiario.data

        pago.monto = form.monto.data
        pago.fecha_pago = form.fecha_pago.data
        pago.tipo_pago = form.tipo_pago.data.lower()
        pago.descripcion = form.descripcion.data

        pagos.editar_pago_db()

        return redirect(
            url_for("pagos.listar_pagos", success="Pago editado exitosamente.")
        )

    return render_template("editar_pago.html", form=form, pago=pago)


@pagos_bp.route("/search", methods=["GET"])
@login_required
@check("pago_index")
def buscar_pagos():
    tipo_pago = (
        request.args.get("tipo_pago").lower() if request.args.get("tipo_pago") else None
    )
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    orden = request.args.get("orden", "asc")
    page = request.args.get(
        "page", 1, type=int
    )  

    pagos_realizado = pagos.buscar_pagos(tipo_pago, fecha_inicio, fecha_fin)

    pagos_realizado = pagos_realizado.order_by(
        Pagos.fecha_pago.asc() if orden == "asc" else Pagos.fecha_pago.desc()
    )

    total_paginas = (pagos_realizado.count() + PAGOS_POR_PAGINA - 1) // PAGOS_POR_PAGINA
    pagos_pag = (
        pagos_realizado.offset((page - 1) * PAGOS_POR_PAGINA)
        .limit(PAGOS_POR_PAGINA)
        .all()
    )

    return render_template(
        "listado_pagos.html",
        pagos_realizado=pagos_pag,
        orden=orden,
        total_paginas=total_paginas,
        pagina_actual=page,
    )
