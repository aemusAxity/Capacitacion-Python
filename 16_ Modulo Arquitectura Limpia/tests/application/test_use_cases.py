from unittest.mock import MagicMock

from app.application.ports import OrderRepository, UnitOfWork
from app.application.use_cases import CrearOrdenUseCase


def test_crear_orden_use_case_con_uow() -> None:
    # 1. Preparación de Mocks
    mock_repo = MagicMock(spec=OrderRepository)
    mock_uow = MagicMock(spec=UnitOfWork)

    # Asignamos el repositorio simulado a la propiedad 'orders' del UoW simulado
    mock_uow.orders = mock_repo

    # Hacemos que el 'with mock_uow:' devuelva el propio mock (comportamiento de __enter__)
    mock_uow.__enter__.return_value = mock_uow

    # 2. Instanciación del Caso de Uso
    caso_de_uso = CrearOrdenUseCase(uow=mock_uow)

    # 3. Ejecución
    items_data = [{"nombre": "Teclado", "precio": 1000.0}]
    orden = caso_de_uso.ejecutar(
        id_orden="200", cliente="Melody", items_data=items_data
    )

    # 4. Comprobaciones de Arquitectura
    # Verificamos que se usó el repositorio
    mock_repo.guardar_orden.assert_called_once_with(orden)
    # Verificamos que se confirmó la transacción
    mock_uow.commit.assert_called_once()
