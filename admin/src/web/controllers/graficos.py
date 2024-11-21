# src/web/controllers/graficos.py
from flask import Blueprint, render_template
from src.core.database import db
from src.core.jya.models import Jinete, TipoDiscapacidad, TiposDiscapacidadEnum
from src.core.ecuestre.ecuestre import Ecuestre
from sqlalchemy import func
from src.web.handlers.auth import login_required

graficos_bp = Blueprint("graficos", __name__, template_folder="../templates/graficos")

@graficos_bp.route("/vista_graficos", methods=["GET"])
@login_required
def vista_graficos():
    # Datos para el gráfico de tipos de discapacidad
    discapacidad_counts = {
        tipo.value: db.session.query(Jinete)
        .join(Jinete.discapacidades)
        .filter(TipoDiscapacidad.tipos_discapacidad == tipo)
        .count()
        for tipo in TiposDiscapacidadEnum
    }

    # Datos para el gráfico de proporción de becados
    becados = db.session.query(db.func.count(Jinete.id)).filter(Jinete.becado == True).scalar()
    no_becados = db.session.query(db.func.count(Jinete.id)).filter(Jinete.becado == False).scalar()
    datos_becados = {"Becados": becados, "No Becados": no_becados}

    # Datos para el gráfico de propuestas de trabajo más solicitadas
    propuestas_data = (
        db.session.query(Ecuestre.tipoJyA, func.count(Ecuestre.id))
        .group_by(Ecuestre.tipoJyA)
        .order_by(func.count(Ecuestre.id).desc())
        .all()
    )
    propuestas = [propuesta[0] for propuesta in propuestas_data]
    cantidades_propuestas = [propuesta[1] for propuesta in propuestas_data]

    return render_template(
        "graficos/vista_graficos.html",
        discapacidad_counts=discapacidad_counts,
        datos_becados=datos_becados,
        propuestas=propuestas,
        cantidades_propuestas=cantidades_propuestas,
    )