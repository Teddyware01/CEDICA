from src.core.database import db
from src.core.contenido import Contenido


def list_contenido():
    contenido = Contenido.query.all()
    return contenido


def create_contenido(**kwargs):
    contenido = Contenido(**kwargs)
    db.session.add(contenido)
    db.session.commit()

    return contenido


