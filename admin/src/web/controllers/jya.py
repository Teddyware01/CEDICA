from flask import Blueprint, render_template, request
from core.jya.models import Jinete, Familiar, SituacionPrevisional, TrabajoInstitucional
#from src.core.equipo.extra_models import Domicilio, ContactoEmergencia
from core.jya.forms import AddJineteForm
from core.jya.models import TipoDiscapacidadEnum
from core import jya

from core.database import db

bp = Blueprint("jya", __name__, url_prefix="/jya")


from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.equipo.models import Empleado, Profesion, PuestoLaboral, CondicionEnum
from src.core.equipo.extra_models import Domicilio, ContactoEmergencia
from src.core.equipo.forms import AddEmpleadoForm
from src.core import equipo

from src.core.database import db

bp = Blueprint("equipo", __name__, url_prefix="/equipo")




@bp.get("/")
def listar_jinetes():
    sort_by = request.args.get("sort_by")
    dni = request.args.get("dni")
    search = request.args.get("search")

    jinetes = Jinete.list_jinetes(
        sort_by=sort_by, dni=dni, search=search
    )
    return render_template(
        "jinete/jinete.html", jinetes=jinetes
    )



@bp.get("/")
def listar_empleados():
    sort_by = request.args.get("sort_by")
    id_puesto_laboral = request.args.get("id_puesto_laboral")
    search = request.args.get("search")

    # usa lo de... src/core/equipo/__init__.py
    empleados = equipo.list_empleados(
        sort_by=sort_by, id_puesto_laboral=id_puesto_laboral, search=search
    )
    puestos_laborales = equipo.list_puestos_laborales()
    return render_template(
        "equipo/equipo.html", empleados=empleados, puestos_laborales=puestos_laborales
    )

