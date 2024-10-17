from src.core.database import db
from src.core.auth.user import Users
from src.core.auth.roles import Roles
from src.core.auth.permisos import Permisos
from src.core.jya.models import Jinete, Familiar
from src.core.equipo.extra_models import Domicilio, ContactoEmergencia, Provincia, Localidad
from sqlalchemy import or_

def list_jinetes(sort_by=None, search=None):
    query = Jinete.query
    if search:
        query = query.filter(
            or_(
                Jinete.nombre.like(f"%{search}%"),
                Jinete.apellido.like(f"%{search}%"),
                Jinete.dni.like(f"%{search}%"),
                Jinete.profesionales.like(f"%{search}%"),
            )
    )
        
    if sort_by:
        if sort_by == "nombre_asc":
            query = query.order_by(Jinete.nombre.asc())
        elif sort_by == "nombre_desc":
            query = query.order_by(Jinete.nombre.desc())
        elif sort_by == "apellido_asc":
            query = query.order_by(Jinete.apellido.asc())
        elif sort_by == "apellido_desc":
            query = query.order_by(Jinete.apellido.desc())
    return query


def create_jinete(**kwargs):
    jinete = Jinete(**kwargs)
    db.session.add(jinete)
    db.session.commit()

    return jinete

def delete_jinete(id):
    jinete = Jinete.query.get(id)
    if jinete:
        db.session.delete(jinete)
        db.session.commit()
        return True
    return False


def edit_jinete(id, **kwargs):
    jinete = Jinete.query.get(id)
    for key, value in kwargs.items():
        if hasattr(jinete, key):
            setattr(jinete, key, value)
    db.session.commit()
    

def traer_jinete(jinete_id): #get_jinete
    jinete = Jinete.query.get(jinete_id)
    return jinete
    
def update_jinete(jinete_id, **kwargs):
    jinete = traer_jinete(jinete_id)
    for key, value in kwargs.items():
        setattr(jinete, key, value)
    db.session.add(jinete)
    db.session.commit()
    
    return jinete


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

def add_direccion(**kwargs):
    direccion = Domicilio(**kwargs)
    db.session.add(direccion)
    db.session.commit()
    return direccion

def list_provincias():
    return Provincia.query.all()

def get_provincia_by_id(provincia_id):
    return Provincia.query.get(provincia_id)

def list_localidades(id_provincia=None):
    query = Localidad.query
    if id_provincia:
        query = query.filter(Localidad.provincia_id == id_provincia)
    return query.all()

def get_localidad_by_id(localidad_id):
    return Localidad.query.get(localidad_id)

def add_familiar(**kwargs):
    familiar = Familiar(**kwargs)
    db.session.add(familiar)
    db.session.commit()
    return familiar