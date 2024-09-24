import pytest
from flask import render_template
from tests import client


@pytest.fixture
def app():



    # Añadir dinámicamente la ruta para las pruebas
    @app.route("/cause_500")
    def cause_500():
        # Provocar un error 500 para la prueba
        return (
            render_template(
                "error.html",
                error=(
                    500,
                    "Error Interno del Servidor",
                    "Ocurrió un error inesperado en el servidor.",
                ),
            ),
            500,
        )

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_error_404(client):
    response = client.get("/ruta-inexistente")
    assert response.status_code == 404
    assert "No Encontrado" in str(response.data)


def test_error_500(client):
    response = client.get("/cause_500")
    assert response.status_code == 500
