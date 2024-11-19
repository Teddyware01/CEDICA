from flask import Blueprint
from flask import flash,render_template, redirect, url_for, request, session
from src.core import auth



bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.get("/")
def login():
    return render_template("auth/login.html")


@bp.post("/authenticate")
def authenticate():
    params = request.form

    user = auth.find_user_by_email_and_password(params["email"], params["password"])
    
    if not user:
        flash("Usuario o contraseña incorrecta", "error")
        return redirect(url_for("auth.login"))
    if not user.activo:
        flash("Tu cuenta está bloqueada. No puedes iniciar sesión.", "error")
        return redirect(url_for("auth.login"))
    session["user"] = user.email
    flash("Sesion iniciada correctamente!", "success")
    return redirect(url_for("auth.login"))

@bp.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("Sesion cerrada correctamente!", "info")
    else:
        flash("No hay una sesion activa!", "error")
    
    return redirect(url_for("auth.login"))
