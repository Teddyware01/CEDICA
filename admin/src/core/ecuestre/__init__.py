from src.core.ecuestre.sedes import Sedes
from src.core.equipo.models import Empleado
from src.core.ecuestre.ecuestre import Ecuestre
from src.core.ecuestre.ecuestre import empleado_ecuestre
from src.core.database import db

def create_sede(**kwargs):
    sede = Sedes(**kwargs)
    db.session.add(sede)
    db.session.commit()

    return sede

def create_ecuestre(**kwargs):
    ecuestre = Ecuestre(**kwargs)
    db.session.add(ecuestre)
    db.session.commit()

    return ecuestre

def list_ecuestre(sort_by=None, search=None):
    query = Ecuestre.query
    if search:
        query = query.filter(
                Ecuestre.nombre.like(f"%{search}%"),   
        )
    if sort_by:
        if sort_by == "nombre_asc":
            query = query.order_by(Ecuestre.nombre.asc())
        elif sort_by == "nombre_desc":
            query = query.order_by(Ecuestre.nombre.desc())
        elif sort_by == "fecha_nacimiento_asc":
            query = query.order_by(Ecuestre.fecha_nacimiento.asc())
        elif sort_by == "fecha_nacimiento_desc":
            query = query.order_by(Ecuestre.fecha_nacimiento.desc())
        elif sort_by == "fecha_ingreso_asc":
            query = query.order_by(Ecuestre.fecha_ingreso.asc())
        elif sort_by == "fecha_ingreso_desc":
            query = query.order_by(Ecuestre.fecha_ingreso.desc())
    return query.all()

def traer_ecuestre(ecuestre_id):
    ecuestre = Ecuestre.query.get(ecuestre_id)
    return ecuestre

def traer_sedes(sede_id):
    sede = Sedes.query.get(sede_id)
    return sede

def traer_id_empleados(caballo_id):
    empleados_ids = (
        db.session.query(empleado_ecuestre.c.empleado_id)
        .filter(empleado_ecuestre.c.ecuestre_id == caballo_id)
        .all()
    )
    empleados_ids = [empleado_id[0] for empleado_id in empleados_ids]
    return empleados_ids



def traer_equipo(ids_miembros):
    print(ids_miembros)
    miembros = Empleado.query.filter(Empleado.id.in_(ids_miembros)).all()
    return miembros

def traer_todosempleados():
    query = Empleado.query
    return query.all()

def asignar_empleado(ecuestre,empleado):
    ecuestre.empleado = empleado
    db.session.add(ecuestre)
    db.session.commit()

    return ecuestre

def edit_encuestre(ecuestre_id, **kwargs):
    Ecuestre = traer_ecuestre(ecuestre_id)
    for key, value in kwargs.items():
        if hasattr(Ecuestre, key):
            setattr(Ecuestre, key, value)
    db.session.commit()

def actualizar_asignados(caballo_id, lista_id):

    ecuestre = Ecuestre.query.get(caballo_id)
    empleados_asignados_ids = {int(empleado_id) for empleado_id in lista_id}
    print(f"Estos son los empleados asignados: {empleados_asignados_ids}")
    # empleados ya asignados
    empleados_actuales = {empleado.id for empleado in ecuestre.empleado}
    print(f"Estos son los empleados actuales: {empleados_actuales}")
    #nuevos empleados a agregar (los que no están en empleados_actuales)
    nuevos_empleados = empleados_asignados_ids - empleados_actuales
    print(f"Estos son los empleados a agregar: {nuevos_empleados}")
    # empleados a eliminar (los que ya no están en empleados_asignados_ids)
    empleados_a_eliminar = empleados_actuales - empleados_asignados_ids
    print(f"Estis son los empleados a eliminar : {empleados_a_eliminar}")
    
    for nuevo_id in nuevos_empleados:
        nuevo_empleado = Empleado.query.get(nuevo_id)
        if nuevo_empleado:
            ecuestre.empleado.append(nuevo_empleado)

    for eliminar_id in empleados_a_eliminar:
        empleado_a_eliminar = Empleado.query.get(eliminar_id)
        if empleado_a_eliminar:
            ecuestre.empleado.remove(empleado_a_eliminar)
    db.session.commit()


def delete_ecuestre(ecuestre_id):
    ecuestre = traer_ecuestre(ecuestre_id)
    if ecuestre:
        db.session.delete(ecuestre)
        db.session.commit()
        return True
    return False