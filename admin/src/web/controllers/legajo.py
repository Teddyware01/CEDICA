from flask import render_template, request, redirect, flash, url_for, current_app
from os import fstat
from flask import Blueprint
from src.core import auth
from src.core.jya import legajo
from src.core.database import db
from src.core.jya.legajo.forms import AddDocumentoForm
from src.core.jya.legajo.models import TipoDocumentoEnum

bp = Blueprint("legajo", __name__, url_prefix="/jinetes/legajo")

@bp.get("/")
def listar_documentos():
    sort_by = request.args.get("sort_by")
    search = request.args.get('search', '')
    documentos = legajo.list_documentos(sort_by=sort_by, search=search)

    return render_template("jya/legajo/listado_documentos.html", documentos=documentos)

@bp.get("/agregar_documento")
def add_documento_form():
    form = AddDocumentoForm()
    form.tipo.choices = [(tipo.name, tipo.value) for tipo in TipoDocumentoEnum]
    
    return render_template("jya/legajo/agregar_documento.html", form=form)

@bp.post("/agregar_documento")
def add_documento():
    form = AddDocumentoForm(request.form)
    legajo.create_documento(
        titulo=request.form["titulo"],
        fecha_subida=request.form["fecha_subida"],
        tipo=request.form["tipo"],
    )
    
    flash("Documento agregado exitosamente", "success")
    return redirect(url_for("legajo.listar_documentos"))