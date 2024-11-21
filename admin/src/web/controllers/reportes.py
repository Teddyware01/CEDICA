# src/web/controllers/reportes.py
from flask import Blueprint, render_template, request
from sqlalchemy import func
from src.core.database import db
from src.core.jya.models import Jinete
from src.core.cobros.models import RegistroCobro
from src.core.equipo.models import Empleado, Profesion, PuestoLaboral
from src.web.handlers.auth import login_required

reportes_bp = Blueprint("reportes", __name__, template_folder="../templates/reportes")

@reportes_bp.route("/reportes", methods=["GET"])
@login_required
def elegir_reporte():
    """Vista para elegir entre diferentes reportes."""
    return render_template("reportes/elegir_reporte.html")

@reportes_bp.route("/historico_cobros", methods=["GET"])
@login_required
def historico_cobros():
    jinete_id = request.args.get("jinete_id")
    
    if not jinete_id:
        return render_template(
            "reportes/historico_cobros.html",
            message="No hay datos suficientes: faltan datos del Jinete o Amazona.",
            cobros=None,
            jinete=None,
        )
    
    jinete = Jinete.query.get(jinete_id)
    if not jinete:
        return render_template(
            "reportes/historico_cobros.html",
            message="No hay datos suficientes: el Jinete o Amazona no existe en el sistema.",
            cobros=None,
            jinete=None,
        )
    
    cobros = (
        db.session.query(RegistroCobro)
        .filter(RegistroCobro.jinete_id == jinete_id)
        .order_by(RegistroCobro.fecha_pago)
        .all()
    )

    if not cobros:
        return render_template(
            "reportes/historico_cobros.html",
            message=f"No hay datos suficientes: no se encontraron cobros registrados para {jinete.nombre} {jinete.apellido}.",
            cobros=None,
            jinete=jinete,
        )

    return render_template(
        "reportes/historico_cobros.html",
        jinete=jinete,
        cobros=cobros,
        message=None,
    )

@reportes_bp.route("/reporte_empleados", methods=["GET"])
@login_required
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

    # Convertir los datos a un formato amigable para la vista
    edad_promedio_dict = {
        actividad.value: round(edad_promedio, 2) if edad_promedio else 0
        for actividad, edad_promedio in edad_promedio_data
    }

    # Renderizar la tabla en la plantilla
    return render_template(
        "reportes/edad_promedio_actividad.html",
        edad_promedio_dict=edad_promedio_dict,
    )
