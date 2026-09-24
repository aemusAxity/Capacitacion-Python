from fastapi.testclient import TestClient

from app.main import app

# Creamos el cliente que simulará ser el navegador o Postman
client = TestClient(app)


def test_crear_orden_exitoso() -> None:
    # 1. Preparamos el JSON que mandaría el usuario
    payload = {
        "id_orden": "500",
        "cliente": "Paul Gonzalez",
        "items": [{"nombre": "Teclado Mecánico", "precio": 1500.0}],
    }

    # 2. Simulamos la petición POST
    response = client.post("/ordenes/", json=payload)

    # 3. Verificamos la respuesta de FastAPI
    assert response.status_code == 200
    datos_respuesta = response.json()
    assert datos_respuesta["mensaje"] == "Orden creada con éxito"
    assert datos_respuesta["total_a_pagar"] == 1500.0


def test_crear_orden_sin_items_da_error() -> None:
    # 1. JSON inválido (sin items)
    payload = {"id_orden": "501", "cliente": "Leila Hernandez", "items": []}

    # 2. Hacemos la petición POST
    response = client.post("/ordenes/", json=payload)

    # 3. Verificamos que devuelva el código 400 y el mensaje de error de nuestro Dominio
    assert response.status_code == 400
    assert "al menos un artículo" in response.json()["detail"]
