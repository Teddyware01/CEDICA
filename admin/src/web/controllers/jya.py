from flask import render_template, request, redirect, flash, url_for
from flask import Blueprint
from src.core import auth
from src.core import jya
from src.core.database import db


bp = Blueprint("jya", __name__, url_prefix="/jinetes")


@bp.get("/")
def listar_jinetes():
    sort_by = request.args.get("sort_by")
    page = request.args.get('page', 1, type=int)
    per_page = 3  
    jinetes = jya.list_jinetes(sort_by=sort_by).paginate(page=page, per_page=per_page)

    return render_template("jya/listado_jya.html", jinetes=jinetes)

@bp.post("/agregar_jinete")
def add_jinete():
    jya.create_jinete(
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        dni=request.form["dni"],
    )
    flash("Jinete agregado exitosamente", "success")
    return render_template("jya/listado_jya.html")

@bp.get("/agregar_jinete")
def agregar_jinete_form():
    return render_template("add_client.html")


@bp.get("/ver_jinete")
def view_jinete():
    return render_template("add_client.html")

@bp.get("/editar_jinete<int:id>")
def edit_jinete_form(id):
    jinete = jya.traer_jinete(id)
    return render_template("edit_client.html", jinete=jinete)


@bp.post("/editar_jinete<int:id>")
def update_jinete(id):
    jya.edit_jinete(
        id,
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        dni=request.form["dni"],
    )
    flash("Jinete actualizado exitosamente", "success")
    return redirect("edit_client.html")


@bp.get("/eliminar_jinete<int:id>")
def delete_jinete_form(id):
    jinete = jya.traer_jinete(id)
    return render_template("delete_client.html", jinete=jinete)


@bp.post("/eliminar_jinete<int:id>")
def delete_jinete(id):
    jya.delete_jinete(id)
    return render_template("jya/listado_jya.html")



