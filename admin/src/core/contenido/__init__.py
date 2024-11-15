from src.core.database import db
from .contenido import Contenido


def list_contenido():
    contenido = Contenido.query.all()
    print("SE LISTA TODO EL CONTENIDO, que son:",len(contenido))
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



