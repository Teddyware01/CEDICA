from flask import render_template, request, redirect, flash, url_for
from flask import Blueprint
from src.core import auth
from src.core.database import db


bp = Blueprint("users", __name__, url_prefix="/listado_De_usuarios")


@bp.get("/")
def listar_usuarios():
    sort_by = request.args.get("sort_by")
    users = auth.list_users(sort_by=sort_by)
    return render_template("listado.html", usuarios=users)


@bp.get("/agregar_cliente")
def add_client_form():
    return render_template("add_client.html")


@bp.get("/editar_cliente<int:user_id>")
def edit_client_form(user_id):
    user = auth.traer_usuario(user_id)
    return render_template("edit_client.html", user=user)


@bp.get("/eliminar_cliente<int:user_id>")
def delete_client_form(user_id):
    user = auth.traer_usuario(user_id)
    return render_template("delete_client.html", user=user)


@bp.post("/agregar_cliente")
def add_client():
    email = request.form["email"]
    if auth.user_email_exists(email):
        flash("El email ya está en uso. Por favor elige otro.", "error")
        return redirect(url_for("users.add_client_form"))
    auth.create_user(
        email=request.form["email"],
        alias=request.form["alias"],
        password=request.form["password"],
        system_admin=request.form.get("is_admin") is not None,
        activo=request.form.get("is_active") is not None,
    )
    flash("Cliente agregado exitosamente", "success")
    return redirect(url_for("users.listar_usuarios"))


@bp.post("/eliminar_cliente<int:user_id>")
def delete_client(user_id):
    auth.delete_user(user_id)
    return redirect(url_for("users.listar_usuarios"))


@bp.post("/editar_cliente<int:user_id>")
def update_user(user_id):
    email = request.form["email"]
    if auth.user_email_exists(email, user_id):
        flash("El email ya está en uso. Por favor elige otro.", "error")
        return redirect(url_for("users.edit_client_form", user_id=user_id))
    auth.edit_user(
        user_id,
        email=request.form["email"],
        alias=request.form["alias"],
        password=request.form["password"],
        system_admin=request.form.get("is_admin") is not None,
        activo=request.form.get("is_active") is not None,
    )

    flash("Usuario actualizado exitosamente", "success")
    return redirect(url_for("users.listar_usuarios"))


@bp.post("/block/<int:user_id>")
def block_user(user_id):
    user = auth.traer_usuario(user_id)
    if user:
        user.activo = False
        db.session.commit()
        flash("Usuario bloqueado con éxito.", "success")
    else:
        flash("Usuario no encontrado.", "danger")
    return redirect(url_for("users.listar_usuarios"))


@bp.post("/activate/<int:user_id>")
def activate_user(user_id):
    user = auth.traer_usuario(user_id)
    if user:
        user.activo = True
        db.session.commit()
        flash("Usuario activado con éxito.", "success")
    else:
        flash("Usuario no encontrado.", "danger")
    return redirect(url_for("users.listar_usuarios"))
