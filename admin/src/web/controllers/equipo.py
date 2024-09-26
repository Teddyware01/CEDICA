# src/web/controllers/equipo.py
from flask import Blueprint, render_template, request
from src.core.equipo import (
    empleado,
)  # creo que aca lo hace gracias al init.py de /equipo
from src.core.equipo import list_empleados

equipo_blueprint = Blueprint("equipo", __name__, url_prefix="/equipo")


@equipo_blueprint.route("/")
def issues_index():
    return render_template("equipo/index.html", empleados=list_empleados)


@equipo_blueprint.route("/equipo/add", methods=["GET"])
def issues_add():  # revisar si deberian tener distinto nombre
    return render_template("equipo/formulario_alta_empleado.html")


@equipo_blueprint.route("/equipo/add", methods=["POST"])
def issues_add():  # revisar si deberian tener distinto nombre
    nuevo_empleado = {
        "id": request.form.get("id"),
        "email": request.form.get("email"),
        # ...COMPLETAR FORMULARIO...
        # CHECKEAR VALIDACIONES DEL FORMULARIO
    }
    empleado.append(nuevo_empleado)
    return render_template(
        "equipo/add_exitoso.html",
    )
