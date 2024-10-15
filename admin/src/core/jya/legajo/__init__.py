from src.core.database import db
from src.core.jya.legajo.models import Documento
from sqlalchemy import or_
from sqlalchemy import cast, String

def list_documentos(sort_by=None, search=None):
    query = Documento.query

    if search:
        query = query.filter(
            Documento.titulo.like(f"%{search}%") |
            cast(Documento.tipo, String).like(f"%{search}%")
        )

    # Ordenamiento basado en sort_by
    if sort_by:
        if sort_by == "titulo_asc":
            query = query.order_by(Documento.titulo.asc())
        elif sort_by == "titulo_desc":
            query = query.order_by(Documento.titulo.desc())
        elif sort_by == "fecha_asc":
            query = query.order_by(Documento.fecha_subida.asc())
        elif sort_by == "fecha_desc":
            query = query.order_by(Documento.fecha_subida.desc())

    return query.all() 


def create_documento(**kwargs):
    documento = Documento(**kwargs)
    db.session.add(documento)
    db.session.commit()

    return documento

def delete_documento(id):
    documento = Documento.query.get(id)
    if documento:
        db.session.delete(documento)
        db.session.commit()
        return True
    return False


def edit_documento(id, **kwargs):
    documento = Documento.query.get(id)
    for key, value in kwargs.items():
        if hasattr(documento, key):
            setattr(documento, key, value)
    db.session.commit()
    

def get_documento(jinete_id): 
    documento = Documento.query.get(jinete_id)
    return documento