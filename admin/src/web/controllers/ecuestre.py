from src.core.database import db
from src.core import ecuestre


from flask import Blueprint, render_template, request, flash, redirect, url_for

bp = Blueprint("ecuestre", __name__, url_prefix="/ecuestre")

@bp.get("/")
def listar_ecuestre():
    sort_by = request.args.get("sort_by")
    search = request.args.get("search")
    page = request.args.get("page", type=int, default=1) 
    ecuestres = ecuestre.list_ecuestre(sort_by=sort_by, search=search, page=page)
    return render_template("ecuestre/listado.html", ecuestre=ecuestres)

@bp.get("/ecuestre<int:ecuestre_id>")
def ver_ecuestre(ecuestre_id):
    caballo = ecuestre.traer_ecuestre(ecuestre_id)
    sedes = ecuestre.traer_sedes(caballo.sede_id)
    ids_empleados = ecuestre.traer_id_empleados(ecuestre_id)
    equipos = ecuestre.traer_equipo(ids_empleados)
    return render_template("ecuestre/ver_ecuestre.html", ecuestre=caballo, sede=sedes, entrenadores=equipos)


@bp.get("/editar_ecuestre<int:ecuestre_id>")
def edit_ecuestre_form(ecuestre_id):
    caballo = ecuestre.traer_ecuestre(ecuestre_id)
    sedes = ecuestre.traer_sedes(caballo.sede_id)
    ids_empleados = ecuestre.traer_id_empleados(ecuestre_id)
    equipos = ecuestre.traer_equipo(ids_empleados)
    todos_empleados = ecuestre.traer_todosempleados()
    return render_template("ecuestre/edit_ecuestre.html", ecuestre=caballo, sede=sedes, entrenadores=equipos, empleados=todos_empleados)

@bp.post("/editar_cliente<int:ecuestre_id>")
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
    ecuestre.edit_encuestre(
        ecuestre_id,
        nombre = request.form["nombre"],
        fecha_nacimiento = request.form["fecha_nacimiento"],
        sexo = sexo,
        raza = request.form["raza"],
        pelaje = request.form["pelaje"],
        fecha_ingreso = request.form["fecha_ingreso"],
        sede_id = sede_id,
    )
   
    entrenadores_asignados = request.form.getlist("entrenadores_asignados")
    ecuestre.actualizar_asignados(ecuestre_id,entrenadores_asignados)

    return redirect(url_for("ecuestre.listar_ecuestre"))

  

@bp.get("/eliminar_ecuestre<int:ecuestre_id>")
def delete_ecuestre_form(ecuestre_id):
    ecuestre_datos = ecuestre.traer_ecuestre(ecuestre_id)
    sedes = ecuestre.traer_sedes(ecuestre_datos.sede_id)
    return render_template("ecuestre/delete_ecuestre.html", ecuestre=ecuestre_datos, sede=sedes)



@bp.post("/eliminar_ecuestre<int:ecuestre_id>")
def delete_ecuestre(ecuestre_id):
    ecuestre.delete_ecuestre(ecuestre_id)
    return redirect(url_for("ecuestre.listar_ecuestre"))


@bp.get("/add_ecuestre")
def add_ecuestre_form():
    todos_empleados = ecuestre.traer_todosempleados()
    return render_template("ecuestre/add_ecuestre.html", empleados=todos_empleados)

@bp.post("/add_ecuestre")
def add_ecuestre():
    sexo = request.form["sexo"],
    if(sexo == "MACHO"):
        sexo = True
    else:
        sexo = False
    nuevo_ecuestre = ecuestre.create_ecuestre(
        nombre = request.form["nombre"],
        fecha_nacimiento = request.form["fecha_nacimiento"],
        sexo = sexo,
        raza = request.form["raza"],
        pelaje = request.form["pelaje"],
        fecha_ingreso = request.form["fecha_ingreso"],
        sede_id = int(request.form["sede"])
    )
    ecuestre_id = nuevo_ecuestre.id
    entrenadores_asignados = request.form.getlist("entrenadores_asignados")
    ecuestre.agregar_empleados(ecuestre_id,entrenadores_asignados)
    flash("Ecuestre agregado exitosamente", "success")
    return redirect(url_for("ecuestre.listar_ecuestre"))
