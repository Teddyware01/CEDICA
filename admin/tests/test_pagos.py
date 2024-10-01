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
