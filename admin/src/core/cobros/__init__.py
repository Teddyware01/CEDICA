from src.core.database import db
from src.core.cobros.models import RegistroCobro
from src.core.equipo.models import Empleado
from src.core.cobros.forms import RegistroCobroForm


def agregar_cobro(nuevo_cobro):
    db.session.add(nuevo_cobro)
    db.session.commit()


def listar_cobros(
    fecha_inicio, fecha_fin, medio_pago, nombre_recibido, apellido_recibido
):
    query = RegistroCobro.query

    if fecha_inicio and fecha_fin:
        query = query.filter(RegistroCobro.fecha_pago.between(fecha_inicio, fecha_fin))

    if medio_pago:
        query = query.filter(RegistroCobro.medio_pago == medio_pago.lower())

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
    if orden == "desc":
        cobros_realizado = query.order_by(RegistroCobro.fecha_pago.desc()).all()
    else:
        cobros_realizado = query.order_by(RegistroCobro.fecha_pago.asc()).all()
    return cobros_realizado


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
    medio_pago, fecha_inicio, fecha_fin, nombre_recibe, apellido_recibe, orden
):

    query = RegistroCobro.query.join(
        Empleado, RegistroCobro.recibido_por == Empleado.id
    )

    if medio_pago:
        query = query.filter(RegistroCobro.medio_pago == medio_pago.lower())
    if fecha_inicio and fecha_fin:
        query = query.filter(RegistroCobro.fecha_pago.between(fecha_inicio, fecha_fin))
    if nombre_recibe:
        query = query.filter(Empleado.nombre.ilike(f"{nombre_recibe}%"))
    if apellido_recibe:
        query = query.filter(Empleado.apellido.ilike(f"{apellido_recibe}%"))
    if orden == "desc":
        query = query.order_by(RegistroCobro.fecha_pago.desc())
    else:
        query = query.order_by(RegistroCobro.fecha_pago.asc())

    return query


def obtener_todos(query):
    return query.all()
