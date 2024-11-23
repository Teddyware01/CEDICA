from flask import render_template, request, redirect, flash, url_for, current_app
from flask import Blueprint
from src.core import auth
from src.core.auth import Users
from src.core.database import db
from src.web.handlers.auth import login_required, check
from src.core.equipo.models import Empleado
from email_validator import validate_email, EmailNotValidError

bp = Blueprint("users", __name__, url_prefix="/listado_De_usuarios")


@bp.get("/pending/")
@login_required
@check("user_accept")
def listar_usuarios_pendientes():    
    sort_by = request.args.get("sort_by")
    search = request.args.get("search")
    page = request.args.get("page", type=int, default=1) 
    status = request.args.get("status")

    pending_users = auth.list_users_pending(sort_by=sort_by, search=search, page=page,status=status)
    return render_template("listado_pendientes.html", usuarios=pending_users)


@bp.get("/pending/<int:user_id>")
@login_required
@check("user_accept")
def atender_pending_user(user_id):
    user = auth.traer_usuario(user_id)
    if user:
        roles = user.roles
        roles_nombres = [rol.nombre for rol in roles]
    roles = auth.traer_roles(user_id)
    empleados_asignables = Empleado.query.filter(Empleado.usuario_asignado == None ).all() #los disponibles(sin asignar)

    # Si tiene uno asignado, que lo muestre en la lista de opciones
    empleado_ya_asignado = user.empleado_asignado
    if empleado_ya_asignado:
        empleados_asignables.append(empleado_ya_asignado)
    
    return render_template("accepting_user.html", user=user, roles=roles, roles_nombres=roles_nombres, empleados_asignables=empleados_asignables, empleado_ya_asignado=empleado_ya_asignado)


@bp.post("/pending/<int:user_id>")
@login_required
@check("user_accept")
def accept_user(user_id):
    auth.edit_user(
        user_id,
        alias=request.form["alias"],
        empleado_id=request.form["empleado_asignado"],
        system_admin=request.form.get("is_admin") is not None,
        activo=request.form.get("is_active") is not None, 
        is_accept_pending=False, 
    )
    selected_roles = request.form.getlist('roles')
    auth.actualizar_roles(user_id,selected_roles)

    flash("Solicitud de 'usuario pendiente' atendida exitosamente", "success")
    return redirect(url_for("users.listar_usuarios_pendientes"))


@bp.get("/")
@login_required
@check("user_index")
def listar_usuarios():    
    sort_by = request.args.get("sort_by")
    search = request.args.get("search")
    page = request.args.get("page", default=1, type=int)  
    status_filter = request.args.get('status')
    role_filter = request.args.getlist('roles')
    exact_match = request.args.get('exact_match', type=bool)
    roles = auth.all_roles()
    roles_nombres = [rol.nombre for rol in roles]
    per_page = current_app.config.get("PAGINATION_PER_PAGE")
    users = auth.list_users(
        status_filter=status_filter,
        role_filter=role_filter,
        exact_match=exact_match,
        sort_by=sort_by,
        search=search,
        page=page,
        per_page=per_page
    )

    return render_template("listado.html", usuarios=users, roles=roles_nombres)

@bp.get("/cliente/<int:user_id>")
@login_required
@check("user_show")
def mostrar_usuario(user_id):
    user = Users.query.get_or_404(user_id)  # Obtener el empleado
    if user:
        roles = auth.traer_roles(user_id)
        roles_asignados = [rol.nombre for rol in roles]
    return render_template("ver_cliente.html", user=user, roles_asignados=roles_asignados)

@bp.get("/agregar_cliente")
@login_required
@check("user_new")
def add_client_form():
    empleados_asignables = Empleado.query.filter(Empleado.esta_borrado == False).all()
    return render_template("add_client.html",empleados_asignables=empleados_asignables)



@bp.post("/agregar_cliente")
@login_required
@check("user_new")
def add_client():
    email = request.form["email"]

    # Validar el email
    try:
        # Se valida y normaliza el email
        valid_email = validate_email(email)
        email = valid_email.email  # Normaliza el email (convierte a minúsculas y corrige algunos errores comunes)

        # Validar que el email termine en .com
        if not email.endswith('.com'):
            flash("El correo electrónico debe terminar en '.com'", "error")
            return redirect(url_for("users.add_client_form"))

    except EmailNotValidError as e:
        flash(f"El correo electrónico no es válido: {str(e)}", "error")
        return redirect(url_for("users.add_client_form"))

    # Verificar si el email ya está en uso
    if auth.user_email_exists(email):
        flash("El email ya está en uso por un usuario. Por favor elige otro.", "error")
        return redirect(url_for("users.add_client_form"))

    if request.form["empleado_asignado"] == '':
        empleado_id = None
    else:
        empleado_id=request.form["empleado_asignado"]
    # Crear el nuevo usuario
    auth.create_user(
        email=email,
        alias=request.form["alias"],
        # Puede o NO tener un empleado asignado, que debe estar registrado primero.
        empleado_id=empleado_id,
        password=request.form["password"],
        system_admin=request.form.get("is_admin") is not None,
        activo=request.form.get("is_active") is not None,
    )

    flash("Cliente agregado exitosamente", "flashes-success")
    return redirect(url_for("users.listar_usuarios"))



@bp.get("/editar_cliente/<int:user_id>")
@login_required
@check("user_update")
def edit_client_form(user_id):
    user = auth.traer_usuario(user_id)
    roles = auth.traer_roles(user_id)
    roles_asignados = [rol.nombre for rol in roles]
    empleados_asignables = Empleado.query.filter( Empleado.esta_borrado == False ).all() #los disponibles(sin asignar)
    empleado_ya_asignado = user.empleado_asignado
    print(f"sus roles son: {roles}")
    if empleado_ya_asignado != None and empleado_ya_asignado.esta_borrado:
        empleado_ya_asignado = None
    return render_template("edit_client.html", user=user, roles=roles_asignados, empleados_asignables=empleados_asignables, empleado_ya_asignado=empleado_ya_asignado)


@bp.get("/eliminar_cliente/<int:user_id>")
@login_required
@check("user_destroy")
def delete_client_form(user_id):
    user = auth.traer_usuario(user_id)
    return render_template("delete_client.html", user=user)



@bp.post("/eliminar_cliente/<int:user_id>")
@login_required
@check("user_destroy")
def delete_client(user_id):
    auth.delete_user(user_id)
    flash("Usuario eliminado exitosamente", "flashes-success")
    return redirect(url_for("users.listar_usuarios"))


@bp.post("/editar_cliente/<int:user_id>")
@login_required
@check("user_update")
def update_user(user_id):
    email = request.form["email"]
    # Validar el email
    try:
        # Se valida y normaliza el email
        valid_email = validate_email(email)
        email = valid_email.email  # Normaliza el email (convierte a minúsculas y corrige algunos errores comunes)
        # Validar que el email termine en .com
        if not email.endswith('.com'):
            flash("El correo electrónico debe terminar en '.com'", "error")
            return redirect(url_for("users.edit_client_form", user_id=user_id))

    except EmailNotValidError as e:
        flash(f"El correo electrónico no es válido: {str(e)}", "error")
        return redirect(url_for("users.edit_client_form", user_id=user_id))

    if auth.user_email_exists(email, user_id):
        flash("El email ya está en uso. Por favor elige otro.", "error")
        return redirect(url_for("users.edit_client_form", user_id=user_id))
    if request.form["empleado_asignado"] == '':
        empleado_id = None
    else:
        empleado_id=request.form["empleado_asignado"]

    auth.edit_user(
        user_id,
        email=request.form["email"],
        alias=request.form["alias"],
        empleado_id=empleado_id,
        password=request.form["password"],
        system_admin=request.form.get("is_admin") is not None,
        activo=request.form.get("is_active") is not None,
    )
    selected_roles = request.form.getlist('roles')
    auth.actualizar_roles(user_id,selected_roles)

    flash("Usuario actualizado exitosamente", "flashes-success")
    return redirect(url_for("users.listar_usuarios"))


@bp.post("/block/<int:user_id>")
@login_required
@check("user_update")
def block_user(user_id):
    user = auth.traer_usuario(user_id)
    if user.system_admin:
        flash("No se puede bloquear un usuario administrador", "flashes-error")
        return render_template("listado.html", usuarios=auth.list_users())
    if user:
        user.activo = False
        db.session.commit()
        flash("Usuario bloqueado con éxito.", "flashes-success")
    else:
        flash("Usuario no encontrado.", "error")
    return redirect(url_for("users.listar_usuarios"))


@bp.post("/activate/<int:user_id>")
@login_required
@check("user_update")
def activate_user(user_id):
    user = auth.traer_usuario(user_id)
    if user:
        user.activo = True
        db.session.commit()
        flash("Usuario activado con éxito.", "success")
    else:
        flash("Usuario no encontrado.", "danger")
    return redirect(url_for("users.listar_usuarios"))

