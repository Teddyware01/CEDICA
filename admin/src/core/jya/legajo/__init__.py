from src.core.database import db
from src.core.jya.models import Documento
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