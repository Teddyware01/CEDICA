from flask import render_template
from dataclasses import dataclass


@dataclass
class Error:
    code: int
    message: str
    description: str


def error_not_found(e):
    error = Error(
        404, "No Encontrado", "La URL solicitada no se encontró en el servidor."
    )
    return render_template("error.html", error=error), error.code


def error_internal_server_error(e):
    error = Error(
        500, "Error Interno del Servidor", "Ocurrió un error inesperado en el servidor."
    )
    return render_template("error.html", error=error), error.code
