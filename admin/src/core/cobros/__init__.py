from src.core.database import db
from src.core.cobros.models import RegistroCobro
from src.core.equipo.models import Empleado
from src.core.jya.models import Jinete
from src.core.cobros.forms import RegistroCobroForm
from src.core.cobros.models import RegistroCobro
from sqlalchemy import or_
from sqlalchemy.orm import aliased

def agregar_cobro(nuevo_cobro):
    db.session.add(nuevo_cobro)
    db.session.commit()


def listar_cobros(
    fecha_inicio=None,
    fecha_fin=None,
    medio_pago=None,
    nombre_recibido=None,
    apellido_recibido=None,
):
    query = db.session.query(RegistroCobro)

    if fecha_inicio and fecha_fin:
        query = query.filter(RegistroCobro.fecha_pago.between(fecha_inicio, fecha_fin))

    if medio_pago:
        query = query.filter_by(medio_pago=medio_pago)

    if nombre_recibido:
        query = query.join(Empleado).filter(
            Empleado.nombre.ilike(f"%{nombre_recibido}%")
        )

    if apellido_recibido:
        query = query.join(Empleado).filter(
            Empleado.apellido.ilike(f"%{apellido_recibido}%")
        )

    return query


def ordenar_fecha(orden, query):
    if orden == "asc":
        return query.order_by(RegistroCobro.fecha_pago.asc())
    else:
        return query.order_by(RegistroCobro.fecha_pago.desc())


def obtener_cobro(id):
    return RegistroCobro.query.get_or_404(id)


def obtener_cobro_param(cobro):
    return RegistroCobroForm(obj=cobro)


def actualizar_cobro():
    db.session.commit()


def eliminar_cobro(cobro):
    db.session.delete(cobro)
    db.session.commit()


def buscar_cobros(
    medio_pago=None,
    fecha_inicio=None,
    fecha_fin=None,
    nombre_recibe=None,
    apellido_recibe=None,
    orden=None,
):
    query = db.session.query(RegistroCobro)

    if medio_pago:
        query = query.filter_by(medio_pago=medio_pago)

    if fecha_inicio and fecha_fin:
        query = query.filter(RegistroCobro.fecha_pago.between(fecha_inicio, fecha_fin))

    if nombre_recibe:
        query = query.join(Empleado).filter(Empleado.nombre.ilike(f"%{nombre_recibe}%"))

    if apellido_recibe:
        query = query.join(Empleado).filter(
            Empleado.apellido.ilike(f"%{apellido_recibe}%")
        )

    if orden == "asc":
        query = query.order_by(RegistroCobro.fecha_pago.asc())
    else:
        query = query.order_by(RegistroCobro.fecha_pago.desc())

    return query


def obtener_todos(query):
    return query

def guardar_cobros_seeds(cobro1, cobro2, cobro3, cobro4, cobro5, cobro6, cobro7, cobro8, cobro9):
    db.session.add(cobro1)
    db.session.add(cobro2)
    db.session.add(cobro3)
    db.session.add(cobro4)
    db.session.add(cobro5)
    db.session.add(cobro6)
    db.session.add(cobro7)
    db.session.add(cobro8)
    db.session.add(cobro9)

    db.session.commit()

def buscar_empleado():
    return aliased(Empleado)

def buscar_empleado_por_id(empleado_alias):
    return db.session.query(RegistroCobro).join(
        empleado_alias, RegistroCobro.recibido_por == empleado_alias.id
        )

def operaciones_filtro(fecha_inicio, fecha_fin, medio_pago, nombre_recibido, apellido_recibido, empleado_alias, query):
    if fecha_inicio and fecha_fin:
        query = query.filter(RegistroCobro.fecha_pago.between(fecha_inicio, fecha_fin))
    if medio_pago:
        query = query.filter(RegistroCobro.medio_pago == medio_pago.lower())
    if nombre_recibido:
        query = query.filter(empleado_alias.nombre.ilike(f"%{nombre_recibido}%"))
    if apellido_recibido:
        query = query.filter(empleado_alias.apellido.ilike(f"%{apellido_recibido}%"))

    return query

def obtener_jinete(jinete_id):
    return Jinete.query.get(jinete_id)  # Asegúrate de que esta consulta se haga correctamente

def obtener_empleado(empleado_id):
    return Empleado.query.filter_by(id=empleado_id).first()
