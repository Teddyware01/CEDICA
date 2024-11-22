from flask import Blueprint, render_template, request, flash, redirect, url_for,abort
from flask import session
from src.core import contenido
from src.web.handlers.auth import check,login_required
from src.core.contenido.contenido import Contenido, TipoContenidoEnum, EstadoContenidoEnum
from src.web.schemas.contenido import contenidos_schema, create_contenido_schema, contenido_schema, publicate_contenido_schema
bp = Blueprint("noticias", __name__, url_prefix="/noticias")
from src.web.api.contenido import contenido
from src.web.handlers.auth import check,login_required, is_authenticated
from src.core.auth import find_user_by_email
from datetime import datetime

tipos_contenido = [tipo.value for tipo in TipoContenidoEnum]

@bp.get("/")
@login_required
@check("noticia_index")
def listar_noticias():
    page = request.args.get("page", type=int, default=1)
    contenidos = contenido.list_contenido(page=page, per_page=5)
    return render_template("contenido/listado_noticia.html", noticias=contenidos)


@bp.get("/add_noticia")
@login_required
@check("noticia_create")
def crear_noticia_form():
    return render_template("contenido/add_noticia.html", tipos_contenido=tipos_contenido)



@bp.post("/add_noticia")
@login_required
@check("noticia_create")
def crear_noticia():
    email = session.get("user") 
    user = find_user_by_email(email)
    user_id = user.id
    attrs = {
            "titulo": request.form.get('titulo'),
            "copete": request.form.get('copete'),
            "contenido": request.form.get('contenido'),
            "tipo": request.form.get('tipo'),
            "autor_user_id": user_id
        }
    tipo_enum = TipoContenidoEnum(attrs["tipo"])
    errors = create_contenido_schema.validate(attrs)
    if errors:
        # Iterar sobre los errores y agregarlos a los mensajes flash
        for field, error_messages in errors.items():
            for error in error_messages:
                flash(f"Error en '{field}': {error}", category="error")
        return render_template("contenido/add_noticia.html", tipos_contenido=tipos_contenido)
    
    # Si no hay errores, crear la noticia
    contenido.create_contenido(titulo=attrs["titulo"],
        copete=attrs["copete"],
        contenido=attrs["contenido"],
        tipo=tipo_enum,
        autor_user_id=attrs["autor_user_id"])

    # Mensaje de éxito
    flash("Noticia creada exitosamente", category="success")
    
    return listar_noticias()

@bp.get("/noticia<int:noticia_id>")
@login_required
@check("noticia_show")
def ver_noticia(noticia_id):
    noticia = contenido.traer_noticia(noticia_id)
    autor = contenido.obtener_usuario_por_id(noticia.autor_user_id)
    return render_template("contenido/ver_noticia.html", noticia=noticia, autor=autor)


@bp.get("/editar_noticia<int:noticia_id>")
@login_required
@check("noticia_update")
def modificar_noticia_form(noticia_id):
    noticia = contenido.traer_noticia(noticia_id)
    return render_template("contenido/update_noticia.html", noticia=noticia, tipos_contenido=tipos_contenido)

@bp.post("/editar_noticia<int:noticia_id>")
@login_required
@check("noticia_update")
def actualizar_noticia(noticia_id):
    noticia = contenido.traer_noticia(noticia_id)
    attrs = {
            "titulo": request.form.get('titulo'),
            "copete": request.form.get('copete'),
            "contenido": request.form.get('contenido'),
            "tipo": request.form.get('tipo'),
        }
    tipo_enum = TipoContenidoEnum(attrs["tipo"])
    errors = contenido_schema.validate(attrs)
    if errors:
        # Iterar sobre los errores y agregarlos a los mensajes flash
        for field, error_messages in errors.items():
            for error in error_messages:
                flash(f"Error en '{field}': {error}", category="error")
        return render_template("contenido/update_noticia.html", noticia=noticia, tipos_contenido=tipos_contenido)
    updated_contenido = contenido.update_contenido(noticia_id, 
        titulo=attrs["titulo"],
        copete=attrs["copete"],
        contenido=attrs["contenido"],
        tipo=tipo_enum,
        autor_user_id=noticia.autor_user_id
    )
    estado = EstadoContenidoEnum("Borrador")
    contenido.actualizar_estado(noticia_id,estado)
    return listar_noticias()

@bp.get("/eliminar_noticia<int:noticia_id>")
@login_required
@check("noticia_destroy")
def eliminar_noticia(noticia_id):
    noticia = contenido.traer_noticia(noticia_id)
    return render_template("contenido/delete_noticia.html", noticia=noticia)

@bp.post("/eliminar_noticia<int:noticia_id>")
@login_required
@check("noticia_destroy")
def confirmar_eliminacion(noticia_id):
    contenido.delete_contenido(noticia_id)
    flash("Noticia borrada exitosamente")
    return listar_noticias()

@bp.get("/archivar<int:noticia_id>")
@login_required
@check("noticia_update")
def archivar(noticia_id):
    estado = EstadoContenidoEnum("Archivado")
    contenido.actualizar_estado(noticia_id,estado)
    flash (f"Archivado exitosamente")
    return listar_noticias()

@bp.get("/recuperar<int:noticia_id>")
@login_required
@check("noticia_update")
def recuperar(noticia_id):
    estado = EstadoContenidoEnum("Borrador")
    contenido.actualizar_estado(noticia_id,estado)
    flash (f"Recuperado  exitosamente")
    return listar_noticias()

@bp.get("/publicar/<int:noticia_id>")
@login_required
@check("noticia_create")
def publicar(noticia_id):
    noticia = contenido.traer_noticia(noticia_id)
    published_at = datetime.now()
    attrs = {
            "titulo": noticia.titulo,
            "copete": noticia.copete,
            "contenido": noticia.contenido,
            "fecha_publicacion": published_at.isoformat(),
            "tipo": noticia.tipo.value,
            "autor_user_id": noticia.autor_user_id
        }

    # Validar los atributos
    errors = publicate_contenido_schema.validate(attrs)
    if errors:
        for field, error_messages in errors.items():
            for error in error_messages:
                flash(f"Error en '{field}': {error}", category="error")
    else:
        tipo_enum = TipoContenidoEnum(attrs["tipo"])
        estado = EstadoContenidoEnum("Publicado")
        contenido.update_contenido(
            noticia_id,
            titulo=attrs["titulo"],
            copete=attrs["copete"],
            contenido=attrs["contenido"],
            tipo=tipo_enum,
            published_at=published_at,
            autor_user_id=noticia.autor_user_id
        )
        contenido.actualizar_estado(noticia_id, estado)
        flash(f"Publicado exitosamente")

    return listar_noticias()


@bp.post("/publicar")
@login_required
@check("noticia_create")
def publicar_add():
    published_at = datetime.now()
    email = session.get("user") 
    user = find_user_by_email(email)
    user_id = user.id
    attrs = {
            "titulo": request.form.get('titulo'),
            "copete": request.form.get('copete'),
            "contenido": request.form.get('contenido'),
            "fecha_publicacion": published_at.isoformat(),  
            "tipo": request.form.get('tipo'),
            "autor_user_id": user_id
        }
    errors = publicate_contenido_schema.validate(attrs)
    if errors:
        # Iterar sobre los errores y agregarlos a los mensajes flash
        for field, error_messages in errors.items():
            for error in error_messages:
                flash(f"Error en '{field}': {error}", category="error")
        return render_template("contenido/add_noticia.html", tipos_contenido=tipos_contenido)
    
    # Si no hay errores, crear la noticia
    tipo_enum = TipoContenidoEnum(attrs["tipo"])
    estado = estado = EstadoContenidoEnum("Publicado")
    contenido.create_contenido(
        titulo=attrs["titulo"],
        copete=attrs["copete"],
        contenido=attrs["contenido"],
        published_at = published_at,
        tipo=tipo_enum,
        estado = estado,
        autor_user_id=attrs["autor_user_id"])

    # Mensaje de éxito
    flash("Noticia Publicada exitosamente", category="success")
    
    return listar_noticias()
