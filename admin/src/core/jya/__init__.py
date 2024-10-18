from src.core.database import db
from src.core.auth.user import Users
from src.core.auth.roles import Roles
from src.core.auth.permisos import Permisos
from src.core.jya.models import Jinete, Familiar, Documento
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

def associate_jinete_familiar(jinete_id, familiar_id):
    # Obtener instancias de Jinete y Familiar
    jinete = Jinete.query.get(jinete_id)
    familiar = Familiar.query.get(familiar_id)

    # Verificar si los objetos fueron recuperados correctamente
    if not jinete or not familiar:
        raise ValueError("Jinete o Familiar no encontrado")

    # Agregar el familiar al jinete usando la relación definida
    jinete.familiares.append(familiar)

    # Guardar los cambios en la base de datos
    db.session.commit()
    

def add_documento(**kwargs):
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

def associate_jinete_documento(jinete_id, documento_id):
    # Obtener instancias de Jinete y Documento
    jinete = Jinete.query.get(jinete_id)
    documento = Documento.query.get(documento_id)

    # Verificar si los objetos fueron recuperados correctamente
    if not jinete or not documento:
        raise ValueError("Jinete o documento no encontrado")

    # Agregar el documento al jinete usando la relación definida
    jinete.documentos.append(documento)

    # Guardar los cambios en la base de datos
    db.session.commit()

def traer_familiares():
    query = Familiar.query
    return query.all()

def agregar_familiar(jinete_id, lista_id_familiares):
    jinete = Jinete.query.get(jinete_id)
    if not jinete:
        raise ValueError("Jinete no encontrado")

    # Obtener todos los familiares de una vez usando `in_` para mejorar el rendimiento
    familiares = Familiar.query.filter(Familiar.id.in_(lista_id_familiares)).all()
    
    # Agregar los familiares a la lista de familiares del jinete
    for familiar in familiares:
        if familiar not in jinete.familiares:
            jinete.familiares.append(familiar)

    db.session.commit()
