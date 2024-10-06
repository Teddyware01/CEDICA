from flask import render_template, request, redirect, flash, url_for
from flask import Blueprint
from src.core import auth
from src.core import jya
from src.core.database import db


bp = Blueprint("jya", __name__, url_prefix="/jinetes")



@bp.get("/")
def listar_jinetes():
    sort_by = request.args.get("sort_by")
    jinetes = jya.list_jinetes(sort_by=sort_by)
    
    return render_template("jya/listado_jya.html", jinetes=jinetes)