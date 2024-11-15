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


