from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_flujo_completo_clean_architecture() -> None:
    payload = {
        "id_orden": "300",
        "cliente": "Leila Hernandez",
        "items": [{"nombre": "Mouse", "precio": 200.0}],
    }

    response = client.post("/ordenes/", json=payload)

    assert response.status_code == 200
    datos = response.json()

    # Verificamos que el Presenter (Interface Adapters) hizo su trabajo
    assert datos["cliente"] == "LEILA HERNANDEZ"  # Debe estar en mayúsculas
    assert datos["total"] == 200.0
    assert datos["eventos_generados"] == 1
