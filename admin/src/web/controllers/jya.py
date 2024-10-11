from flask import render_template, request, redirect, flash, url_for, current_app
from os import fstat
from flask import Blueprint
from src.core import auth
from src.core import jya
from src.core.database import db
from src.core.jya.forms import AddJineteForm

bp = Blueprint("jya", __name__, url_prefix="/jinetes")


@bp.get("/")
def listar_jinetes():
    sort_by = request.args.get("sort_by")
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 3  
    jinetes = jya.list_jinetes(sort_by=sort_by, search=search).paginate(page=page, per_page=per_page)

    return render_template("jya/listado_jya.html", jinetes=jinetes)

@bp.get("/agregar_jinete")
def add_jinete_form():
    return render_template("jya/agregar_jya.html")


@bp.post("/agregar_jinete")
def add_jinete():
    #form = AddJineteForm(request.form)
    jya.create_jinete(
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        dni=request.form["dni"],
        edad=request.form["edad"],
        fecha_nacimiento=request.form["fecha_nacimiento"],
        telefono=request.form["telefono"],
        #becado=form.condicion.data,
        #observaciones=form.observaciones.data,
        #certificado_discapacidad=form.certificado_discapacidad.data,
        #beneficiario_pension=form.beneficiario_pension.data,
        #tipo_pension=form.tipo_pension.data,
        #profesionales=form.profesionales.data,
    )

    flash("Jinete registrado exitosamente", "success")
    return redirect(url_for("jya.listar_jinetes"))

@bp.get("/ver_jinete<int:jinete_id>")
def view_jinete(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    return render_template("jya/ver_jya.html", jinete=jinete)

@bp.get("/editar_jinete<int:jinete_id>")
def edit_jinete_form(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    return render_template("jya/editar_jya.html", jinete=jinete)

@bp.post("/editar_jinete<int:jinete_id>")
def editar_jinete(jinete_id):
    jya.edit_jinete(
        jinete_id,
        nombre=request.form["nombre"],
        apellido=request.form["apellido"],
        dni=request.form["dni"],
        telefono=request.form["telefono"],
        fecha_nacimiento=request.form["fecha_nacimiento"],
    )
    flash("Jinete actualizado exitosamente", "success")
    return redirect(url_for("jya.listar_jinetes"))

@bp.get("/eliminar_jinete<int:jinete_id>")
def delete_jinete_form(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    return render_template("jya/eliminar_jya.html", jinete=jinete)

@bp.post("/eliminar_jinete<int:jinete_id>")
def delete_jinete(jinete_id):
    jya.delete_jinete(jinete_id)
    return redirect(url_for("jya.listar_jinetes"))

@bp.get("/<int:jinete_id>/edit")
def edit(jinete_id):
    jinete = jya.traer_jinete(jinete_id)
    
    return render_template("jya/edit.html", jinete=jinete)

@bp.post("/<int:jinete_id>/update")
def update(jinete_id):
    params = request.form.copy()
    
    if "avatar" in request.files:
        file = request.files["avatar"]
        client = current_app.storage.client
        size = fstat(file.fileno()).st_size
        #ulid = u.new()
        
        client.put_object(
            "grupo15", file.filename, file, size, content_type=file.content_type
        )           #f"avatars/{ulid}-{file.filename}",
        params["avatar"] = file.filename #Hacer funcion para que genere nombres unicos para el archivo y guardarlo en el usuario. Libreria ULID
                                
    jya.update_jinete(jinete_id, **params)
    flash("Usuario modificado correctamente", "success")
    
    return redirect(url_for("jya.listar_jinetes"))