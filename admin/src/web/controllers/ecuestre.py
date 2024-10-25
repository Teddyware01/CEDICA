from src.core.database import db
from datetime import timedelta
from src.core import ecuestre
from flask import current_app
from os import fstat
import re

from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.web.handlers.auth import check,login_required
bp = Blueprint("ecuestre", __name__, url_prefix="/ecuestre")

@bp.get("/")
@login_required
@check("ecuestre_index")
def listar_ecuestre():
    sort_by = request.args.get("sort_by")
    search = request.args.get("search")
    page = request.args.get("page", type=int, default=1) 
    ecuestres = ecuestre.list_ecuestre(sort_by=sort_by, search=search, page=page)
    return render_template("ecuestre/listado.html", ecuestre=ecuestres)


@bp.get("/ecuestre<int:ecuestre_id>")
@login_required
@check("ecuestre_show")
def ver_ecuestre(ecuestre_id):
    caballo = ecuestre.traer_ecuestre(ecuestre_id)
    sedes = ecuestre.traer_sedes(caballo.sede_id)
    ids_empleados = ecuestre.traer_id_empleados(ecuestre_id)
    equipos = ecuestre.traer_equipo(ids_empleados)
    page = request.args.get('page', 1, type=int)
    documentos_paginated = ecuestre.traerdocumento(ecuestre_id, page=page)
    active_tab = request.args.get('tab', 'general')
    return render_template("ecuestre/ver_ecuestre.html", ecuestre=caballo, sede=sedes, entrenadores=equipos, documentos=documentos_paginated.items, pagination=documentos_paginated, active_tab=active_tab)


@bp.get("/editar_ecuestre<int:ecuestre_id>")
@login_required
@check("ecuestre_update")
def edit_ecuestre_form(ecuestre_id):
    caballo = ecuestre.traer_ecuestre(ecuestre_id)
    sedes = ecuestre.traer_sedes(caballo.sede_id)
    ids_empleados = ecuestre.traer_id_empleados(ecuestre_id)
    equipos = ecuestre.traer_equipo(ids_empleados)
    todos_empleados = ecuestre.traer_todosempleados()
    return render_template("ecuestre/edit_ecuestre.html", ecuestre=caballo, sede=sedes, entrenadores=equipos, empleados=todos_empleados)

@bp.post("/editar_ecuestre<int:ecuestre_id>")
@login_required
@check("ecuestre_update")
def update_ecuestre(ecuestre_id):
    sede_input = request.form["sede_id"]
    sexo = request.form["sexo"]
    if sexo == "true":
        sexo = True
    else:
        sexo = False
    if sede_input == "CASJ":
        sede_id = 1
    elif sede_input == "HLP":
        sede_id = 2
    elif sede_input == "OTRO":
        sede_id = 3
    else:
        sede_id = None 
    nombre = request.form["nombre"]
    raza = request.form["raza"]
    pelaje = request.form["pelaje"]
    fields_to_validate = {
        "Nombre": nombre,
        "Raza": raza,
        "Pelaje": pelaje,
    }
    if not validate_fields(fields_to_validate):
        return edit_ecuestre_form(ecuestre_id)        
    ecuestre.edit_encuestre(
        ecuestre_id,
        nombre = request.form["nombre"],
        fecha_nacimiento = request.form["fecha_nacimiento"],
        sexo = sexo,
        raza = request.form["raza"],
        pelaje = request.form["pelaje"],
        fecha_ingreso = request.form["fecha_ingreso"],
        tipoJyA = request.form["tipoJyA"],
        sede_id = sede_id,
    )
   
    entrenadores_asignados = request.form.getlist("entrenadores_asignados")
    ecuestre.actualizar_asignados(ecuestre_id,entrenadores_asignados)

    return redirect(url_for("ecuestre.listar_ecuestre"))

  

@bp.get("/eliminar_ecuestre<int:ecuestre_id>")
@login_required
@check("ecuestre_destroy")
def delete_ecuestre_form(ecuestre_id):
    ecuestre_datos = ecuestre.traer_ecuestre(ecuestre_id)
    sedes = ecuestre.traer_sedes(ecuestre_datos.sede_id)
    return render_template("ecuestre/delete_ecuestre.html", ecuestre=ecuestre_datos, sede=sedes)



@bp.post("/eliminar_ecuestre<int:ecuestre_id>")
@login_required
@check("ecuestre_destroy")
def delete_ecuestre(ecuestre_id):
    ecuestre.delete_ecuestre(ecuestre_id)
    return redirect(url_for("ecuestre.listar_ecuestre"))


@bp.get("/add_ecuestre")
@login_required
@check("ecuestre_create")
def add_ecuestre_form():
    todos_empleados = ecuestre.traer_todosempleados()
    return render_template("ecuestre/add_ecuestre.html", empleados=todos_empleados)

@bp.post("/add_ecuestre")
@login_required
@check("ecuestre_create")
def add_ecuestre():
    sexo = request.form["sexo"]
    if(sexo == "MACHO"):
        sexo = True
    else:
        sexo = False
    nombre = request.form["nombre"]
    raza = request.form["raza"]
    pelaje = request.form["pelaje"]
    fields_to_validate = {
        "Nombre": nombre,
        "Raza": raza,
        "Pelaje": pelaje,
    }
    if not validate_fields(fields_to_validate):
        return add_ecuestre_form()
    nuevo_ecuestre = ecuestre.create_ecuestre(
        nombre = nombre,
        fecha_nacimiento = request.form["fecha_nacimiento"],
        sexo = sexo,
        raza = raza,
        pelaje = pelaje,
        fecha_ingreso = request.form["fecha_ingreso"],
        tipoJyA = request.form["tipoJyA"],
        sede_id = int(request.form["sede"])
    )
    ecuestre_id = nuevo_ecuestre.id
    entrenadores_asignados = request.form.getlist("entrenadores_asignados")
    ecuestre.agregar_empleados(ecuestre_id,entrenadores_asignados)
    flash("Ecuestre agregado exitosamente", "success")
    return redirect(url_for("ecuestre.listar_ecuestre"))


@bp.get("/editar_ecuestre/documentos<int:ecuestre_id>")
@login_required
@check("ecuestre_update")
def subir_archivo_form(ecuestre_id):
    caballo = ecuestre.traer_ecuestre(ecuestre_id)
    return render_template("ecuestre/add_documento.html", ecuestre=caballo)

@bp.post("/editar_ecuestre/documentos<int:ecuestre_id>")
@login_required
@check("ecuestre_update")
def agregar_documento(ecuestre_id):
    file = request.files["documento"] 
    extensiones_permitidas = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'txt'}
    extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    if extension not in extensiones_permitidas:
        flash("Tipo de archivo no permitido. Solo se permiten archivos: png, jpg, pdf, doc, xls, ppt, odt, txt.", "error")
        return subir_archivo_form(ecuestre_id)
    tamano_maximo = 10 * 1024 * 1024
    size = fstat(file.fileno()).st_size
    if size > tamano_maximo:
        flash(f"El archivo excede el tamaño máximo permitido de {tamano_maximo / (1024 * 1024)} MB.", "error")
        return subir_archivo_form(ecuestre_id)
    existe = ecuestre.ya_tiene_ese_documento(ecuestre_id, file.filename)
    if(existe):
        flash(f"El archivo ya se encuentra almacenado")
        return subir_archivo_form(ecuestre_id)
    nuevo_nombre_archivo = f"ecuestre_{ecuestre_id}_{file.filename}"
    client = current_app.storage.client
    client.put_object("grupo15", nuevo_nombre_archivo, file, size, content_type=file.content_type)    
    ecuestre.crear_documento(
        titulo=file.filename,
        nombre_asignado=request.form["nombre_asignado"], 
        tipo=request.form["tipo_archivo"], 
        ecuestre_id=ecuestre_id
    )  
    return redirect(url_for("ecuestre.ver_ecuestre",ecuestre_id=ecuestre_id))




@bp.get("/editar_ecuestre/<int:ecuestre_id>/documentos/<string:file_name>")
@login_required
@check("ecuestre_show")
def mostrar_archivo(ecuestre_id, file_name):
    nuevo_nombre_archivo = f"ecuestre_{ecuestre_id}_{file_name}"
    expiration = timedelta(seconds=120)
    client = current_app.storage.client
    url =  client.presigned_get_object("grupo15", nuevo_nombre_archivo, expires=expiration) # Esto sirve para archivos sensibles como documento de jya.
    return False

@bp.post("/ecuestre/<int:ecuestre_id>/documento/<int:documento_id>/eliminar")
@login_required
@check("ecuestre_update")
def eliminar_documento(ecuestre_id, documento_id):
    documento = ecuestre.traerdocumentoporid(documento_id)
    if not documento.is_enlace:
        client = current_app.storage.client
        nuevo_nombre_archivo = f"ecuestre_{ecuestre_id}_{documento.titulo}"
        client.remove_object("grupo15", nuevo_nombre_archivo)
    ecuestre.eliminar_documento(documento_id)
    flash("Documento eliminado correctamente.", "success")
    return redirect(url_for('ecuestre.ver_ecuestre', ecuestre_id=ecuestre_id, tab='documentos'))

@bp.get("/ecuestre/<int:ecuestre_id>/documento/<int:documento_id>/eliminar")
@login_required
@check("ecuestre_update")
def eliminar_documento_form(ecuestre_id, documento_id):
    ecuestre_datos = ecuestre.traer_ecuestre(ecuestre_id)
    documento = ecuestre.traerdocumentoporid(documento_id)
    return render_template("ecuestre/delete_documento.html", ecuestre=ecuestre_datos, doc=documento)




def validate_fields(fields):
    # Expresión regular que permite letras, tildes, diéresis y espacios
    pattern = r"^[A-Za-zÁÉÍÓÚáéíóúÜüÑñ\s]+$"
    for field_name, field_value in fields.items():
        if not re.match(pattern, field_value):
            print(f"El campo a analizar es: {field_name}")  # Mensaje de depuración
            flash(f"El campo '{field_name}' con valor '{field_value}' solo puede contener letras.", "error")
            return False
    return True





# EDITAR ARCHIVO GET
@bp.get("/ecuestre/<int:ecuestre_id>/documento/<int:documento_id>/editar")
@login_required
@check("ecuestre_update")
def edit_documento_form(ecuestre_id, documento_id):
    documento = ecuestre.traerdocumentoporid(documento_id)
    return render_template("ecuestre/edit_documento.html", documento=documento, ecuestre_id=ecuestre_id)


# EDITAR ARCHIVO POST
@bp.post("/ecuestre/<int:ecuestre_id>/documento/<int:documento_id>/editar")
@login_required
@check("ecuestre_update")
def editar_documento(ecuestre_id, documento_id):
    nombre_asignado = request.form.get("nombre_asignado")
    tipo = request.form.get("tipo_archivo")

    if not nombre_asignado:
        flash("Debe ingresar un titulo de documento.", "error")
        return redirect(url_for("ecuestre.edit_documento_form", form=request.form, documento_id=documento_id))
    
    if not tipo:
        flash("Debe seleccionar un tipo de documento.", "error")
        return redirect(url_for("ecuestre.edit_documento_form", form=request.form, documento_id=documento_id))
    
    ecuestre.edit_documento(documento_id=documento_id,ecuestre_id=ecuestre_id, nombre_asignado=nombre_asignado, tipo=tipo)
    flash("Documento editado exitosamente", "success")
    return redirect(url_for("ecuestre.ver_ecuestre", ecuestre_id=ecuestre_id))



# ENLACES
# agregar enlace GET
@bp.get("/ecuestre/<int:ecuestre_id>/enlace")
@login_required
@check("ecuestre_update")
def subir_enlace_form(ecuestre_id):    
    ecu = ecuestre.traer_ecuestre(ecuestre_id=ecuestre_id)

    return render_template("ecuestre/add_enlace.html", ecuestre=ecu)

# agregar enlace POST
@login_required
@check("ecuestre_update")
@bp.post("/ecuestre/<int:ecuestre_id>/enlace")
def agregar_enlace(ecuestre_id):
    ecuestre.crear_documento_tipo_enlace(
        ecuestre_id=ecuestre_id,
        url_enlace = request.form["url_enlace"],
        nombre_asignado=request.form["nombre_asignado"]
    ) 
    return redirect(url_for("ecuestre.ver_ecuestre", ecuestre_id=ecuestre_id))



# EDITAR enlace GET
@bp.get("/ecuestre/<int:ecuestre_id>/documento/<int:documento_id>/editar_enlace")
@login_required
@check("ecuestre_update")
def edit_enlace_form(ecuestre_id, documento_id):
    documento = ecuestre.traerdocumentoporid(documento_id)
    return render_template("ecuestre/edit_enlace.html", documento=documento, ecuestre_id=ecuestre_id)

# EDITAR enlace POST
@bp.post("/ecuestre/<int:ecuestre_id>/documento/<int:documento_id>/editar_enlace")
@login_required
@check("ecuestre_update")
def editar_enlace(ecuestre_id, documento_id):
    nombre_asignado = request.form.get("nombre_asignado")
    url_enlace = request.form.get("url_enlace")

    if not nombre_asignado:
        flash("Debe ingresar un titulo de documento.", "error")
        return redirect(url_for("ecuestre.edit_enlace_form", form=request.form, documento_id=documento_id))
    
    if not url_enlace:
        flash("Debe ingresar una url para el enlace.", "error")
        return redirect(url_for("ecuestre.edit_enlace_form", form=request.form, documento_id=documento_id))
    
    ecuestre.edit_documento(documento_id=documento_id,ecuestre_id=ecuestre_id, nombre_asignado=nombre_asignado, url_enlace=url_enlace)
    flash("Documento editado exitosamente", "success")
    return redirect(url_for("ecuestre.ver_ecuestre", ecuestre_id=ecuestre_id))
