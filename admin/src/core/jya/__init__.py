from src.core.database import db
from src.core.auth.user import Users
from src.core.auth.roles import Roles
from src.core.auth.permisos import Permisos
from src.core.jya.models import (Jinete, Familiar, Dias, JineteDocumento,
                                TiposDiscapacidadEnum, DiasEnum,DiagnosticoEnum, 
                                AsignacionEnum,PensionEnum,TrabajoEnum,SedeEnum,
                                TipoDiscapacidad, EscolaridadEnum)
from src.core.equipo.extra_models import Domicilio, ContactoEmergencia, Provincia, Localidad
from sqlalchemy import String, cast, or_



def list_jinetes(sort_by=None, nombre=None, apellido=None, dni=None, profesionales=None, page=1, per_page=None):
    query = Jinete.query
    if nombre:
        query = query.filter(Jinete.nombre.ilike(f"%{nombre}%"))
    if apellido:
        query = query.filter(Jinete.apellido.ilike(f"%{apellido}%"))
    if dni:
        query = query.filter(Jinete.dni.ilike(f"%{dni}%"))
    if profesionales:
        query = query.filter(Jinete.profesionales.ilike(f"%{profesionales}%"))
    if sort_by:
        if sort_by == "nombre_asc":
            query = query.order_by(Jinete.nombre.asc())
        elif sort_by == "nombre_desc":
            query = query.order_by(Jinete.nombre.desc())
        elif sort_by == "apellido_asc":
            query = query.order_by(Jinete.apellido.asc())
        elif sort_by == "apellido_desc":
            query = query.order_by(Jinete.apellido.desc())
        
    paginated_query = query.paginate(page=page, per_page=per_page, error_out=False)
    return paginated_query

def create_jinete(**kwargs):
    jinete = Jinete(**kwargs)
    db.session.add(jinete)
    db.session.commit()

    return jinete

def jinete_dni_exists(dni, jinete_id=None):
    query = Jinete.query.filter_by(dni=dni)
    if jinete_id:
        query = query.filter(Jinete.id != jinete_id)
    return query.first() is not None
    
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
    jinete = Jinete.query.get_or_404(jinete_id)
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

 
def edit_familiar(familiar_id, **kwargs):
    familiar = Familiar.query.get(familiar_id)
    for key, value in kwargs.items():
        if hasattr(familiar, key):
            setattr(familiar, key, value)
    db.session.commit()

def get_primer_familiar(jinete_id):
    jinete = Jinete.query.get(jinete_id)
    return jinete.familiares[0]


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
    
def add_dias(**kwargs):
    dias = Dias(**kwargs)
    db.session.add(dias)
    db.session.commit()
    return dias

def associate_jinete_dias(jinete_id, dias_id):
    # Obtener instancias de Jinete y Dias
    jinete = Jinete.query.get(jinete_id)
    dias = Dias.query.get(dias_id)

    if not jinete or not dias:
        raise ValueError("Jinete o Dias no encontrado")

    jinete.dias.append(dias)
    db.session.commit()



def associate_jinete_dias_name(jinete_id, dia_name):
    jinete = traer_jinete(jinete_id)
    dia = Dias.query.filter_by(dias=dia_name).first()

    if not jinete :
        raise ValueError("Jinete no encontrado")
    if not dia:
        raise ValueError("Dia no encontrado")

    jinete.dias.append(dia)
    db.session.commit()


    
def add_discapacidades(**kwargs):
    discapacidades = TipoDiscapacidad(**kwargs)
    db.session.add(discapacidades)
    db.session.commit()
    return discapacidades

def associate_jinete_discapacidad_id(jinete_id, discapacidad_id):
    jinete = traer_jinete(jinete_id)
    discapacidad = TipoDiscapacidad.query.get(discapacidad_id)

    if not jinete or not discapacidad:
        raise ValueError("Jinete o discapacidades no encontrado")

    jinete.discapacidades.append(discapacidad)
    db.session.commit()


def associate_jinete_discapacidad_name(jinete_id, discapacidad_name):
    jinete = traer_jinete(jinete_id)
    discapacidad = TipoDiscapacidad.query.filter_by(tipos_discapacidad=discapacidad_name).first()

    if not jinete :
        raise ValueError("Jinete  no encontrado")
    if not discapacidad:
        raise ValueError("Discapacidad no encontrada")

    jinete.discapacidades.append(discapacidad)
    db.session.commit()



def clear_jinete_discapacidades(jinete_id):
    jinete = traer_jinete(jinete_id)
    jinete.discapacidades = []
    db.session.commit()

def get_jinete_dias(jinete_id):
    # Fetch the jinete object by its ID
    jinete = Jinete.query.get(jinete_id)
    
    # Check if the jinete exists
    if not jinete:
        return None  # Or raise an exception if preferred

    # Extract the days assigned to the jinete
    assigned_dias = [dia.dias.value for dia in jinete.dias]  # Accessing the 'dias' Enum value

    return assigned_dias


def clear_jinete_dias(jinete_id):
    jinete = traer_jinete(jinete_id)
    jinete.dias = []
    db.session.commit()


def add_documento(**kwargs):
    is_enlace=False
    documento = JineteDocumento(is_enlace=is_enlace,**kwargs)
    db.session.add(documento)
    db.session.commit()
    return documento


def add_documento_tipo_enlace(**kwargs):
    is_enlace=True
    titulo_documento=None
    documento = JineteDocumento(is_enlace=is_enlace, titulo_documento=titulo_documento, **kwargs)
    db.session.add(documento)
    db.session.commit()
    return documento



def delete_documento(documento_id):
    documento = get_documento(documento_id)
    db.session.delete(documento)
    db.session.commit()
    
def edit_documento(documento_id, **kwargs):
    documento = get_documento(documento_id)
    for key, value in kwargs.items():
        if hasattr(documento, key):
            setattr(documento, key, value)
    db.session.commit()
    
def get_documento(documento_id): 
    documento = JineteDocumento.query.get(documento_id)
    return documento

def associate_jinete_documento(jinete_id, documento_id):
    # Obtener instancias de Jinete y Documento
    jinete = Jinete.query.get(jinete_id)
    documento = JineteDocumento.query.get(documento_id)

    # Verificar si los objetos fueron recuperados correctamente
    if not jinete or not documento:
        raise ValueError("Jinete o documento no encontrado")

    # Agregar el documento al jinete usando la relación definida
    jinete.documentos.append(documento)

    # Guardar los cambios en la base de datos
    db.session.commit()



'''def traer_familiares():
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
'''

def traer_documentos(jinete_id, page=1, per_page=10, sort_by=None, search=None):
    # Inicializar el query filtrando por el jinete_id
    query = JineteDocumento.query.filter(JineteDocumento.jinete_id == jinete_id)

    # Agregar la funcionalidad de búsqueda si existe un término de búsqueda
    if search:
        query = query.filter(
            JineteDocumento.nombre_archivo.like(f"%{search}%") |
            cast(JineteDocumento.tipo_documento, String).like(f"%{search}%")
        )

    # Agregar la funcionalidad de ordenamiento basada en el valor de sort_by
    if sort_by:
        if sort_by == "titulo_asc":
            query = query.order_by(JineteDocumento.nombre_archivo.asc())
        elif sort_by == "titulo_desc":
            query = query.order_by(JineteDocumento.nombre_archivo.desc())
        elif sort_by == "fecha_asc":
            query = query.order_by(JineteDocumento.fecha_subida_documento.asc())
        elif sort_by == "fecha_desc":
            query = query.order_by(JineteDocumento.fecha_subida_documento.desc())

    # Retornar los resultados paginados
    return query.paginate(page=page, per_page=per_page, error_out=False)

def traer_documento_id(documento_id):
    documento = JineteDocumento.query.get_or_404(documento_id)
    return documento


def delete_documento(documento_id):
    documento = traer_documento_id(documento_id)
    db.session.delete(documento)
    db.session.commit()


def list_discapacidades():
    return [(tipo.name,tipo.value) for tipo in TiposDiscapacidadEnum]


def list_jinete_tipos_discapacidades(jinete_id):
    jinete = traer_jinete(jinete_id)
    return [{'name': disc.tipos_discapacidad.name, 'value': disc.tipos_discapacidad.value} for disc in jinete.discapacidades]

def get_tipos_discapacidades(jinete_id):
    jinete = Jinete.query.get(jinete_id)
    
    if not jinete:
        return []  

    assigned_discapacidades = [disc.tipos_discapacidad.value for disc in jinete.discapacidades]

    return assigned_discapacidades

def list_dias_semana():
    return  [(dia.name,dia.value) for dia in DiasEnum]

def list_jinete_dias_semana(jinete_id):
    jinete = traer_jinete(jinete_id)
    return [{'name': dia.dias.name, 'value': dia.dias.value} for dia in jinete.dias]

def list_tipos_diagnostico():
    return  [(diagnostico.name, diagnostico.value) for diagnostico in DiagnosticoEnum]

def list_tipos_asignacion():
    return  [(asignacion.name, asignacion.value )for asignacion in AsignacionEnum]

def list_tipos_pensiones():
    return  [(pension.name, pension.value )for pension in PensionEnum]

def list_nivel_escolaridad():
    return  [(esc.name, esc.value )for esc in EscolaridadEnum]
    

def list_familiares_por_jinete(jinete_id):
    jinete = traer_jinete(jinete_id=jinete_id)
    familiares = []
    if jinete:
        familiares = jinete.familiares
    return familiares


def list_trabajo_institucional():
    return  [(trabajo.name, trabajo.value) for trabajo in TrabajoEnum]
    
def list_sedes():
    return  [(sede.name, sede.value) for sede in SedeEnum]
