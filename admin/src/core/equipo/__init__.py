# src/core/equipo/__init__.py
from src.core.database import db
from src.core.equipo.models import Empleado
from src.core.equipo.models import Profesion, PuestoLaboral
from src.core.equipo.extra_models import ContactoEmergencia, Domicilio


# Tabla Empleado


def list_empleados(sort_by=None):
    query = Empleado.query
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
    return query.all()


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
    domicilio = PuestoLaboral(**kwargs)
    db.session.add(domicilio)
    db.session.commit()
    return domicilio
