from src.core.pagos.forms import Empleado
from src.core.database import db
from src.core.pagos.models import Pago as Pagos
from datetime import datetime

def obtener_empleado(form):
    # Asegurarse de obtener una instancia del empleado, no una consulta
    return Empleado.query.filter_by(id=form.beneficiario.data, esta_borrado=False).first()



def agregar_pago(nuevo_pago):
    db.session.add(nuevo_pago)
    db.session.commit()

def ordenar_pagos(orden="asc", tipo_pago="", fecha_inicio=None, fecha_fin=None):
    query = Pagos.query

    if tipo_pago:
        query = query.filter(Pagos.tipo_pago == tipo_pago)
    if fecha_inicio:
        query = query.filter(Pagos.fecha_pago >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Pagos.fecha_pago <= fecha_fin)

    if orden == "asc":
        query = query.order_by(Pagos.fecha_pago.asc())
    else:
        query = query.order_by(Pagos.fecha_pago.desc())

    return query.all()



def eliminar_pago(pago):
    db.session.delete(pago)
    db.session.commit()


def obtener_pago(id):
    return Pagos.query.get_or_404(id)


def editar_pago_db():
    db.session.commit()


def buscar_pagos(tipo_pago, fecha_inicio, fecha_fin):
    query = Pagos.query

    if tipo_pago:
        query = query.filter(db.func.lower(Pagos.tipo_pago) == tipo_pago)
    if fecha_inicio and fecha_fin:
        query = query.filter(Pagos.fecha_pago.between(fecha_inicio, fecha_fin))

    return query

def guardar_pagos_seeds (pagos_datos):
    for pago in pagos_datos:
        nuevo_pago = Pagos(
            beneficiario=pago["beneficiario"],
            monto=pago["monto"],
            fecha_pago=pago["fecha_pago"],
            tipo_pago=pago["tipo_pago"],
            descripcion=pago["descripcion"],
        )
        db.session.add(nuevo_pago)
    db.session.commit()

def validacion_fecha_inicio(fecha_inicio):
    if fecha_inicio:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        except ValueError:
            fecha_inicio = None
    return fecha_inicio

def validacion_fecha_fin(fecha_fin):
    if fecha_fin:
        try:
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            fecha_fin = None
    return fecha_fin
