#src/core/equipo/__init__.py
from src.core.database import db
from src.core.equipo.models import Empleado
from src.core.equipo.models import Profesion, PuestoLaboral
from src.core.equipo.extra_models import ObraSocial


# Tabla Empleado
def list_empleados():
    empleados = Empleado.query.all()
    return empleados


def create_empleado(**kwargs):
    empleado = Empleado(**kwargs)
    db.session.add(empleado)
    db.session.commit()

    return empleado


# otras tablas
def list_profesiones():
    profesiones = Profesion.query.all()
    return profesiones


def list_puestos_laborales():
    puestos_laborales = PuestoLaboral.query.all()
    return puestos_laborales


def list_obras_sociales(**kwargs):
    obras_sociales = ObraSocial.query.all()
    return obras_sociales


def add_profesion(**kwargs):
    profesion = Profesion(**kwargs)
    db.session.add(profesion)
    db.session.commit()
    return profesion


def add_puesto_laboral(**kwargs):
    puesto_laboral = PuestoLaboral(**kwargs)
    db.session.add(puesto_laboral)
    db.session.commit()
    return puesto_laboral


def add_obra_social(**kwargs):
    obra_social = ObraSocial(**kwargs)
    db.session.add(obra_social)
    db.session.commit()
    return obra_social
