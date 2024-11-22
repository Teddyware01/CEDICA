from flask import Blueprint, render_template, request, flash, redirect, url_for,abort
from flask import session
from src.core import contenido
from src.web.handlers.auth import check,login_required
from src.core.contenido.contenido import Contenido, TipoContenidoEnum, EstadoContenidoEnum
from src.web.schemas.contenido import contenidos_schema, create_contenido_schema, contenido_schema
bp = Blueprint("noticias", __name__, url_prefix="/noticias")
from src.web.api.contenido import contenido
from src.web.handlers.auth import check,login_required, is_authenticated
from src.core.auth import find_user_by_email

tipos_contenido = [tipo.value for tipo in TipoContenidoEnum]

@bp.get("/")
def listar_noticias():
    contenidos = contenido.list_contenido()
    print(contenidos)
    return render_template("contenido/listado_noticia.html", noticias=contenidos)


@bp.get("/add_noticia")
def crear_noticia_form():
    return render_template("contenido/add_noticia.html", tipos_contenido=tipos_contenido)

@bp.post("/add_noticia")
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
    print(tipo_enum)
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
def ver_noticia(noticia_id):
    noticia = contenido.traer_noticia(noticia_id)
    autor = contenido.obtener_usuario_por_id(noticia.autor_user_id)
    return render_template("contenido/ver_noticia.html", noticia=noticia, autor=autor)


@bp.get("/editar_noticia<int:noticia_id>")
def modificar_noticia_form(noticia_id):
    return render_template("contenido/listado_noticia.html")


@bp.get("/eliminar_noticia<int:noticia_id>")
def eliminar_noticia(noticia_id):
    return render_template("contenido/listado_noticia.html")

