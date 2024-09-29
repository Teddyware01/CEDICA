from flask import render_template, request, redirect, flash, url_for
from flask import Blueprint
from src.core import auth


bp = Blueprint("users", __name__, url_prefix="/listado_De_usuarios")


@bp.get('/')
def listar_usuarios():
    users = auth.list_users()
    return render_template("listado.html", usuarios=users)

@bp.post('/')
def add_client():
    auth.create_user(
        email = request.form['email'],
        alias = request.form['alias'],
        password = request.form['password'],
        system_admin = request.form.get('is_admin') is not None,  
        activo = request.form.get('is_active') is not None ,
    )
    flash('Cliente agregado exitosamente', 'success')
    return redirect(url_for('users.listar_usuarios'))  