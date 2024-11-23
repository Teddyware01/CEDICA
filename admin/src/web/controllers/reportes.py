# src/web/controllers/reportes.py
from flask import Blueprint, render_template, request
from sqlalchemy import func
from src.core.database import db
from src.core.jya.models import Jinete
from src.core.cobros.models import RegistroCobro
from src.core.equipo.models import Empleado, Profesion, PuestoLaboral
from src.web.handlers.auth import login_required, check

reportes_bp = Blueprint("reportes", __name__, template_folder="../templates/reportes")

@reportes_bp.route("/reportes", methods=["GET"])
@login_required
@check("reporte_show")
def elegir_reporte():
    """Vista para elegir entre diferentes reportes."""
    return render_template("reportes/elegir_reporte.html")


@reportes_bp.route('/grafico_diagnostico')
@login_required
@check("reporte_show")
def grafico_diagnostico():
    datos_diagnostico = db.session.query(Jinete.diagnostico, func.count(Jinete.id)).group_by(Jinete.diagnostico).all()
    diagnosticos = {diagnostico.name: count for diagnostico, count in datos_diagnostico}
    return render_template('grafico_diagnostico.html', diagnosticos=diagnosticos)


@reportes_bp.route("/reporte_empleados", methods=["GET"])
@login_required
@check("reporte_show")
def reporte_empleados():
    empleados_data = (
        db.session.query(
            PuestoLaboral.nombre.label("puesto"),
            Profesion.nombre.label("profesion"),
            db.func.count(Empleado.id).label("cantidad")
        )
        .join(Empleado, Empleado.puesto_laboral_id == PuestoLaboral.id)
        .join(Profesion, Empleado.profesion_id == Profesion.id)
        .group_by(PuestoLaboral.nombre, Profesion.nombre)
        .order_by(PuestoLaboral.nombre, Profesion.nombre)
        .all()
    )

    return render_template(
        "reportes/vista_reporte_empleados.html",
        empleados_data=empleados_data,
    )

@reportes_bp.route("/edad_promedio_actividad", methods=["GET"])
@login_required
@check("reporte_show")
def edad_promedio_por_actividad():
    # Consultar las edades promedio agrupadas por tipo de actividad
    edad_promedio_data = (
        db.session.query(
            Jinete.trabajo_institucional,  # Tipo de actividad
            func.avg(Jinete.edad).label("edad_promedio")  # Edad promedio
        )
        .group_by(Jinete.trabajo_institucional)
        .all()
    )

    # Redondear la edad promedio al número entero más cercano
    edad_promedio_dict = {
        actividad.value: round(edad_promedio) if edad_promedio else 0
        for actividad, edad_promedio in edad_promedio_data
    }

    # Renderizar la tabla en la plantilla
    return render_template(
        "reportes/edad_promedio_actividad.html",
        edad_promedio_dict=edad_promedio_dict,
    )
