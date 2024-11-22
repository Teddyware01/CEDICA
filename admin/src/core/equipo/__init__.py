# src/core/equipo/__init__.py
from src.core.database import db
from src.core.equipo.models import Empleado, Empleado_docs
from src.core.ecuestre.ecuestre import empleado_ecuestre
from src.core.equipo.models import Profesion, PuestoLaboral
from src.core.equipo.extra_models import (
    ContactoEmergencia,
    Domicilio,
    Provincia,
    Localidad,
)

from sqlalchemy import or_


# DOCUMENTOS de EMPLEADOS:

def crear_documento(**kwargs):
    is_enlace=False
    documento = Empleado_docs(is_enlace=is_enlace,**kwargs)
    db.session.add(documento)
    db.session.commit()
    return documento


def traer_documentos(empleado_id, page=1, per_page=3):
    documentos = Empleado_docs.query.filter(Empleado_docs.empleado_id == empleado_id).paginate(page=page, per_page=per_page, error_out=False)
    return documentos

def traer_documento_por_id(documento_id):
    documento = Empleado_docs.query.get_or_404(documento_id)
    return documento



def delete_documento(documento_id):
    documento = traer_documento_por_id(documento_id)
    db.session.delete(documento)
    db.session.commit()


def edit_documento(documento_id, **kwargs):
    documento = traer_documento_por_id(documento_id)
    for key, value in kwargs.items():
        if hasattr(documento, key):
            setattr(documento, key, value)
    db.session.commit()




def crear_documento_tipo_enlace(**kwargs):
    is_enlace=True
    titulo=None
    documento = Empleado_docs(is_enlace=is_enlace, titulo=titulo, **kwargs)
    db.session.add(documento)
    db.session.commit()
    return documento


# Tabla Provincia
def list_provincias():
    return Provincia.query.all()


def get_provincia_by_id(provincia_id):
    return Provincia.query.get(provincia_id)


# Tabla Localidad
# Retorna todas las localidades, o las de una provincia si se le pasa el id_provincia.
def list_localidades(id_provincia=None):
    query = Localidad.query
    if id_provincia:
        query = query.filter(Localidad.provincia_id == id_provincia)
    return query.all()


def get_localidad_by_id(localidad_id):
    return Localidad.query.get(localidad_id)


# Tabla Empleado
def list_empleados(sort_by=None, id_puesto_laboral=None, search=None,page=1, per_page=3):
    query = Empleado.query.filter_by(esta_borrado=False)
    if id_puesto_laboral and id_puesto_laboral != "cualquiera":
        query = query.filter(Empleado.puesto_laboral_id == id_puesto_laboral)
    # Filtrar por término de búsqueda
    if search:
        query = query.filter(
            or_(
                Empleado.nombre.ilike(f"%{search}%"),
                Empleado.apellido.ilike(f"%{search}%"),
                Empleado.dni.ilike(f"%{search}%"),
                Empleado.email.ilike(f"%{search}%"),
            )
        )
    if sort_by:
        if sort_by == "nombre_asc":
            query = query.order_by(Empleado.nombre.asc())
        elif sort_by == "nombre_desc":
            query = query.order_by(Empleado.nombre.desc())
        elif sort_by == "apellido_asc":
            query = query.order_by(Empleado.apellido.asc())
        elif sort_by == "apellido_desc":
            query = query.order_by(Empleado.apellido.desc())
        elif sort_by == "created_at_asc":
            query = query.order_by(Empleado.fecha_inicio.asc())
        elif sort_by == "created_at_desc":
            query = query.order_by(Empleado.fecha_inicio.desc())

    paginated_query = query.paginate(page=page, per_page=per_page, error_out=False)
    return paginated_query


def list_auxiliares_pista():
    auxiliar = PuestoLaboral.query.filter_by(nombre="Auxiliar de pista").first()
    if auxiliar:
        return Empleado.query.filter(Empleado.puesto_laboral_id == auxiliar.id, Empleado.esta_borrado == False).all()
    return []

def list_conductores_caballos():
    conductor = PuestoLaboral.query.filter_by(nombre="Conductor").first()
    if conductor:
        return Empleado.query.filter(Empleado.puesto_laboral_id == conductor.id, Empleado.esta_borrado == False).all()
    return []

def list_terapeutas_y_profesores():
    terapeuta = PuestoLaboral.query.filter_by(nombre="Terapeuta").first()
    profesor = PuestoLaboral.query.filter_by(nombre="Profesor/a").first()

    empleados = []

    if terapeuta:
        empleados += Empleado.query.filter(Empleado.puesto_laboral_id == terapeuta.id, Empleado.esta_borrado==False).all()
    if profesor:
        empleados += Empleado.query.filter(Empleado.puesto_laboral_id == profesor.id, Empleado.esta_borrado==False).all()

    return empleados


def traer_empleado(empleado_id):
    return  Empleado.query.get_or_404(empleado_id)

def create_empleado(**kwargs):
    empleado = Empleado(**kwargs)
    db.session.add(empleado)
    db.session.commit()

    return empleado


def delete_empleado(user_id):
    empleado = Empleado.query.get(user_id)
    if empleado:
        db.session.delete(empleado)
        db.session.commit()
        return True
    return False


def edit_empleado(user_id, **kwargs):
    empleado = Empleado.query.get(user_id)
    for key, value in kwargs.items():
        if hasattr(empleado, key):
            setattr(empleado, key, value)
    db.session.commit()


# Tabla Profesiones
def list_profesiones():
    profesiones = Profesion.query.all()
    return profesiones


def add_profesion(**kwargs):
    profesion = Profesion(**kwargs)
    db.session.add(profesion)
    db.session.commit()
    return profesion


# Tabla PuestoLaboral
def list_puestos_laborales():
    puestos_laborales = PuestoLaboral.query.all()
    return puestos_laborales


def add_puesto_laboral(**kwargs):
    puesto_laboral = PuestoLaboral(**kwargs)
    db.session.add(puesto_laboral)
    db.session.commit()
    return puesto_laboral


# Tabla ContactoEmergencia
def add_contacto_emergencia(**kwargs):
    contacto_emergencia = ContactoEmergencia(**kwargs)
    db.session.add(contacto_emergencia)
    db.session.commit()
    return contacto_emergencia


# Tabla Domiclio
def add_domiclio(**kwargs):
    domicilio = Domicilio(**kwargs)
    db.session.add(domicilio)
    db.session.commit()
    return domicilio

def borrar_tabla_intermedia(empleado_id):
   # Obtener las relaciones filtrando dinámicamente
    relaciones = (
        db.session.query(empleado_ecuestre)
        .filter(empleado_ecuestre.c.empleado_id == empleado_id)
    )

    # Eliminar relaciones directamente
    relaciones.delete(synchronize_session=False)

    # Confirmar los cambios
    db.session.commit()
