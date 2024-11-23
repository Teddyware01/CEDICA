from src.core.database import db
from .contenido import Contenido
from src.core.auth import Users
from src.core.auth import traer_usuario

from .contenido import EstadoContenidoEnum

def list_contenido(page=1, per_page=3):
    query = db.session.query(Contenido, Users.alias).join(Users, Contenido.autor_user_id == Users.id)
    paginated_query = query.paginate(page=page, per_page=per_page, error_out=False)
    return paginated_query

def list_contenido_published():
    contenido = Contenido.query.filter_by(estado=EstadoContenidoEnum.PUBLICADO).all()
    print("SE LISTA TODO EL CONTENIDO <<PUBLISHED>>, que son:", len(contenido))
    return contenido


def get_contenido_id(id):
    contenido = Contenido.query.get(id)
    if not contenido:
        return {"error": "Contenido no encontrado"}, 404
    return contenido

def get_contenido_id(id):
    contenido = Contenido.query.get(id)
    if not contenido:
        return {"error": "Contenido no encontrado"}, 404
    return contenido

def create_contenido(**kwargs):
    contenido = Contenido(**kwargs)
    db.session.add(contenido)
    db.session.commit()
    
    return contenido

def update_contenido(id, **kwargs):
    contenido = Contenido.query.get(id)
    if not contenido:
        return {"error": "Contenido no encontrado"}, 404
    
    for key, value in kwargs.items():
        setattr(contenido, key, value)
    
    db.session.commit()

    return contenido


def delete_contenido(id):
    contenido = Contenido.query.get(id)
    if not contenido:
        return {"error": "Contenido no encontrado"}, 404
    db.session.delete(contenido)
    db.session.commit()

    return {"message": "Contenido eliminado exitosamente"}

def obtener_usuario_por_id(id):
    user = traer_usuario(id)
    if user:
        return user
    return None

def traer_noticia(noticia_id):
    noticia = Contenido.query.get(noticia_id)
    return noticia

def actualizar_estado(noticia_id, estado):
    contenido = Contenido.query.get(noticia_id)
    contenido.estado = estado
    db.session.commit()
    return contenido