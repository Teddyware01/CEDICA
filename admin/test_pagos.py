import pytest
from src.web import create_app
from src.core.database import db
from src.core.pagos import pagos

@pytest.fixture
def app():
    app = create_app('testing')  # Usa una configuración específica para pruebas
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Base de datos en memoria
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos
        yield app
        db.session.remove()
        db.drop_all()  # Eliminar las tablas después de las pruebas

@pytest.fixture
def client(app):
    return app.test_client()  # Cliente de prueba que simula peticiones HTTP

def test_registrar_pago(client):
    # Simular un POST para registrar un nuevo pago
    response = client.post("/", data={
        "beneficiario": "Juan Perez",
        "monto": 100.0,
        "fecha_pago": "2023-10-01",
        "tipo_pago": "Transferencia",
        "descripcion": "Pago de servicio",
    })

    # Verificar que la respuesta sea una redirección después del registro
    assert response.status_code == 302

    # Verificar que el pago se haya registrado en la base de datos
    pago_registrado = pagos.query.filter_by(beneficiario="Juan Perez").first()
    assert pago_registrado is not None
    assert pago_registrado.monto == 100.0

def test_obtener_pagos(client):
    # Registrar un pago para tener datos que recuperar
    client.post("/", data={
        "beneficiario": "Ana Gomez",
        "monto": 150.0,
        "fecha_pago": "2023-09-20",
        "tipo_pago": "Efectivo",
        "descripcion": "Pago en tienda",
    })

    # Realizar un GET para obtener los pagos registrados
    response = client.get("/")
    assert response.status_code == 200
    assert b"Ana Gomez" in response.data  # Verificar que se muestra en la respuesta

def test_eliminar_pago(client):
    # Primero registrar un pago
    client.post("/", data={
        "beneficiario": "Carlos Sanchez",
        "monto": 300.0,
        "fecha_pago": "2023-08-01",
        "tipo_pago": "Cheque",
        "descripcion": "Pago de proveedor",
    })

    # Obtener el pago registrado
    pago = pagos.query.filter_by(beneficiario="Carlos Sanchez").first()

    # Simular una petición DELETE para eliminar el pago
    response = client.delete(f"/{pago.id}")

    # Verificar que el pago haya sido eliminado
    assert response.status_code == 302  # La eliminación redirige
    pago_eliminado = pagos.query.get(pago.id)
    assert pago_eliminado is None  # El pago debe haber sido eliminado

def test_buscar_pagos(client):
    # Registrar pagos para buscar
    client.post("/", data={
        "beneficiario": "Luis Martinez",
        "monto": 200.0,
        "fecha_pago": "2023-10-01",
        "tipo_pago": "Transferencia",
        "descripcion": "Pago de alquiler",
    })

    client.post("/", data={
        "beneficiario": "Pedro Fernandez",
        "monto": 50.0,
        "fecha_pago": "2023-09-01",
        "tipo_pago": "Efectivo",
        "descripcion": "Pago de café",
    })

    # Buscar pagos por tipo
    response = client.get("/search", query_string={"tipo_pago": "Transferencia"})
    assert response.status_code == 200
    assert b"Luis Martinez" in response.data
    assert b"Pedro Fernandez" not in response.data  # Solo se deben mostrar los pagos de Transferencia

    # Buscar pagos por rango de fechas
    response = client.get("/search", query_string={
        "fecha_inicio": "2023-09-01",
        "fecha_fin": "2023-10-01"
    })
    assert b"Luis Martinez" in response.data
    assert b"Pedro Fernandez" in response.data  # Ambos deben aparecer en el rango
