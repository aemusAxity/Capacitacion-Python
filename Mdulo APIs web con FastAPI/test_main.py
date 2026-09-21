import pytest
from db_temporal import Base, engine
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Dejamos la DB limpia
@pytest.fixture(autouse=True)
def limpiar_base_de_datos():

    # 1 Borra la BD
    Base.metadata.drop_all(bind=engine)
    # 2 Crearla en blanco
    Base.metadata.create_all(bind=engine)

    # Ejecuta el test
    yield


def test_acceso_denegado_sin_token():
    respuesta = client.get("/api/v1/orders/")
    assert respuesta.status_code == 401


def test_flujo_completo_integracion():

    # 1. Hacer Login para obtener el token
    respuesta_login = client.post(
        "/login", data={"username": "admin", "password": "secreto"}
    )
    assert respuesta_login.status_code == 200
    token = respuesta_login.json()["access_token"]

    # 2. Configurar la cabecera con el Token
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Crear una orden
    nueva_orden = {"producto": "Silla Ergonómica", "cantidad": 1}
    respuesta_post = client.post("/api/v1/orders/", json=nueva_orden, headers=headers)
    assert respuesta_post.status_code == 200

    # 4. Leer las órdenes para comprobar que se guardó en la DB
    respuesta_get = client.get("/api/v1/orders/", headers=headers)
    assert respuesta_get.status_code == 200

    datos_db = respuesta_get.json()
    assert len(datos_db) == 1
    assert datos_db[0]["producto"] == "Silla Ergonómica"
