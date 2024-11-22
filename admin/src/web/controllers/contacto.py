from src.core.contacto.forms import AddConsultaForm
from flask import Blueprint, render_template, request, jsonify, current_app, redirect, flash, url_for
from src.core import contacto
from src.core.contacto.models import Contacto
from src.core.database import db
from src.web.handlers.auth import login_required,check


bp = Blueprint("contacto", __name__, url_prefix="/contacto")


@bp.get("/")
@login_required
@check("contacto_index")
def listar_consultas():
    sort_by = request.args.get("sort_by")
    search = request.args.get("search")
    page = request.args.get("page", type=int, default=1) 
    consultas = contacto.list_consultas(sort_by=sort_by, search=search, page=page)
    return render_template("contacto/listar_consultas.html", consultas=consultas)


@bp.get("/agregar_consulta")
@login_required
@check("contacto_create")
def agregar_consulta():

    form = AddConsultaForm()
    return render_template("contacto/agregar_consulta.html", form=form)


@bp.post("/agregar_consulta")
@login_required
@check("contacto_create")
def add_consulta():
    form = AddConsultaForm(request.form)

    if form.validate_on_submit():
        contacto.add_consulta(
            nombre=form.nombre.data,
            email=form.email.data,
            mensaje=form.mensaje.data,
            estado=form.estado.data,
            comentario=form.comentario.data,
        )

        # Guardar todo en la base de datos
        db.session.commit()

        flash("Consulta registrada exitosamente", "success")
        return redirect(url_for("contacto.listar_consultas"))

    else:
        flash("Por favor corrija los errores en el formulario:", "error")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en el campo {field}: {error}", "danger")

    return render_template("contacto/agregar_consulta.html", form=form)


@bp.get("/ver_consulta/<int:consulta_id>")
@login_required
@check("contacto_show")
def view_consulta(consulta_id):
    consulta = contacto.traer_consulta(consulta_id)
    page=request.args.get("page", 1, type=int)
    active_tab=request.args.get("tab", "general")
    sort_by = request.args.get("sort_by")
    search = request.args.get("search")
    return render_template("contacto/ver_consulta.html", consulta=consulta, active_tab=active_tab)


@bp.get("/eliminar_consulta/<int:consulta_id>")
@login_required
@check("contacto_destroy")
def delete_consulta_form(consulta_id):
    consulta = contacto.traer_consulta(consulta_id)
    return render_template("contacto/eliminar_consulta.html", consulta=consulta)


@bp.post("/eliminar_consulta/<int:consulta_id>")
@login_required
@check("contacto_destroy")
def delete_consulta(consulta_id):
    contacto.delete_consulta(consulta_id)
    
    return redirect(url_for("contacto.listar_consultas"))


@bp.get("/editar_consulta/<int:consulta_id>")
@login_required
@check("contacto_update")
def edit_consulta_form(consulta_id):
    consulta = contacto.traer_consulta(consulta_id)
    form = AddConsultaForm(obj=consulta) 

    form.nombre.data = consulta.nombre
    form.email.data = consulta.email
    form.mensaje.data = consulta.mensaje
    form.estado.data = consulta.estado
    estado_actual =  contacto.list_estados()
    form.comentario.data = consulta.comentario

    return render_template("contacto/editar_consulta.html", form=form, consulta=consulta, estado_actual=estado_actual)


@bp.post("/editar_consulta/<int:consulta_id>")
@login_required
@check("contacto_update")
def editar_consulta(consulta_id):
    consulta = contacto.traer_consulta(consulta_id)
    form = AddConsultaForm(request.form, obj=consulta)

    if form.validate_on_submit():
        form.populate_obj(consulta)
        db.session.commit()

        flash("Consulta editada exitosamente", "success")
        return redirect(url_for("contacto.view_consulta", consulta_id=consulta.id))

    else:
        flash("Por favor corrija los errores en el formulario:", "error")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en el campo {field}: {error}", "danger")

    return render_template("contacto/editar_consulta.html", form=form, consulta=consulta)



@bp.post("/verify-captcha")
def verify_captcha():
    secret_key = "6LcD3n4qAAAAAI1RssEtVWIAtuaBn25ebGctDRr5"
    captcha_response = request.json.get("captchaResponse")

    verification_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret": secret_key, "response": captcha_response}
    response = request.post(verification_url, data=payload)
    result = response.json()

    if result.get("success"):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": result.get("error-codes")})


@bp.post('/submit_form')
def submit_form():
    if not request.json:
        return jsonify({'error': 'Bad request'}), 400

    try:
        nombre = request.json.get('nombre')
        email = request.json.get('email')
        mensaje = request.json.get('mensaje')

        nuevo_mensaje = Contacto(nombre=nombre, email=email, mensaje=mensaje)
        db.session.add(nuevo_mensaje)
        db.session.commit()

        return jsonify({'mensaje': 'Mensaje enviado con éxito!'}), 200
    except Exception as e:
        current_app.logger.error(f'Failed to insert message: {e}')
        return jsonify({'error': 'Internal server error'}), 500