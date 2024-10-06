from flask import Blueprint, render_template, request
from core.jya.models import Jinete, Familiar, SituacionPrevisional, TrabajoInstitucional
#from src.core.equipo.extra_models import Domicilio, ContactoEmergencia
from core.jya.forms import AddJineteForm
from core.jya.models import TipoDiscapacidadEnum
from core import jya

from core.database import db

bp = Blueprint("jya", __name__, url_prefix="/jya")


from core.database import db


@bp.get("/")
def listar_jinetes():
    sort_by = request.args.get("sort_by")
    search = request.args.get("search")

    jinetes = jya.list_jinetes(
        sort_by=sort_by, search=search
    )
    return render_template(
        "jya/listado_jya.html", jinetes=jinetes
    )