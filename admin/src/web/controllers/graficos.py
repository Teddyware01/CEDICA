# src/web/controllers/graficos.py
from flask import Blueprint, render_template
from src.core.database import db
from src.core.jya.models import Jinete, TipoDiscapacidad, TiposDiscapacidadEnum
from src.core.ecuestre.ecuestre import Ecuestre
from src.core.cobros.models import RegistroCobro
from src.core.pagos.models import Pago
from sqlalchemy import func
from src.web.handlers.auth import login_required, check

graficos_bp = Blueprint("graficos", __name__, template_folder="../templates/graficos")

@graficos_bp.route("/vista_graficos", methods=["GET"])
@login_required
@check("grafico_show")
def vista_graficos():
    # Datos para el gráfico de pagos por beneficiario
    pagos_data = (
        db.session.query(Pago.beneficiario, func.sum(Pago.monto))
        .group_by(Pago.beneficiario)
        .order_by(func.sum(Pago.monto).desc())
        .all()
    )
    beneficiarios = [pago[0] for pago in pagos_data]
    montos = [pago[1] for pago in pagos_data]

    # Datos para el gráfico de proporción de becados
    becados = db.session.query(db.func.count(Jinete.id)).filter(Jinete.becado == True).scalar()
    no_becados = db.session.query(db.func.count(Jinete.id)).filter(Jinete.becado == False).scalar()
    datos_becados = {"Becados": becados, "No Becados": no_becados}

    rangos = ["$1000-", "$1000-$5000", "$5000-$10000", "$10000-$20000", "$20000+"]
    rangos_monto = [
        (0, 1000),
        (1000, 5000),
        (5000, 10000),
        (10000, 20000),
        (20000, float("inf"))
    ]

    cobros_por_rango = []
    for rango in rangos_monto:
        count = (
            db.session.query(RegistroCobro)
            .filter(RegistroCobro.monto >= rango[0], RegistroCobro.monto < rango[1])
            .filter(RegistroCobro.monto.isnot(None))  # Asegurarnos de que no haya valores nulos
            .count()
        )
        cobros_por_rango.append(count)

    return render_template(
        "graficos/vista_graficos.html",
        beneficiarios=beneficiarios,
        montos=montos,
        datos_becados=datos_becados,
        rangos=rangos,
        cobros_por_rango=cobros_por_rango,
    )
