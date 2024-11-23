from src.core.database import db
from src.core.contacto.models import Contacto, EstadoEnum
from sqlalchemy import or_


def list_consultas(sort_by=None, search=None, page=1, per_page=None):
    query = Contacto.query

    # Filtrar por término de búsqueda
    if search:
        query = query.filter(
            or_(
                Contacto.estado.ilike(f"%{search}%"),
            )
        )
    
    if sort_by:
        if sort_by == "fecha_asc":
            query = query.order_by(Contacto.fecha_creacion.asc())
        elif sort_by == "fecha_desc":
            query = query.order_by(Contacto.fecha_creacion.desc())

    paginated_query = query.paginate(page=page, per_page=per_page, error_out=False)
    return paginated_query



def traer_consulta(consulta_id):
    return  Contacto.query.get_or_404(consulta_id)
    
def add_consulta(**kwargs):
    consulta = Contacto(**kwargs)
    db.session.add(consulta)
    db.session.commit()

    return consulta


def delete_consulta(consulta_id):
    consulta = Contacto.query.get(consulta_id)
    if consulta:
        db.session.delete(consulta)
        db.session.commit()
        return True
    return False


def edit_consulta(consulta_id, **kwargs):
    consulta = Contacto.query.get(consulta_id)
    for key, value in kwargs.items():
        if hasattr(consulta, key):
            setattr(consulta, key, value)
    db.session.commit()
    
def list_estados():
    return  [(est.name, est.value) for est in EstadoEnum]