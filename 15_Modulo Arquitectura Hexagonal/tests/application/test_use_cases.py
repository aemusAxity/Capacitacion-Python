from unittest.mock import MagicMock

from app.application.ports import OrderRepository
from app.application.use_cases import CrearOrdenUseCase


def test_crear_orden_use_case() -> None:
    # MagicMock Finge ser un OrderRepository"
    repo_mock = MagicMock(spec=OrderRepository)

    # Le pasamos nuestro magicmock que finge ser el repo
    caso_de_uso = CrearOrdenUseCase(repositorio=repo_mock)

    # Ejecutamos
    datos_items = [{"nombre": "Silla", "precio": 3000.0}]
    orden_creada = caso_de_uso.ejecutar(
        id_orden="300", cliente="Paul", items_data=datos_items
    )

    assert orden_creada.total == 3000.0

    # Assertions del MagicMock (La magia de MagicMock):
    # En vez de revisar una lista, le preguntamos directamente al mock si el Caso de Uso lo mandó llamar
    repo_mock.guardar_orden.assert_called_once()

    # Incluso podemos preguntarle si fue llamado exactamente con la orden correcta
    repo_mock.guardar_orden.assert_called_with(orden_creada)
