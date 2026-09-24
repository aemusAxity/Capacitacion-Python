import pytest
from app.domain.order import Order, OrderItem
from app.infrastructure.unit_of_work import MemoriaUnitOfWork


def test_uow_commit_guarda_datos_exitosamente() -> None:
    # 1. Preparación
    uow = MemoriaUnitOfWork()
    orden = Order(id="1", cliente="Aerin", items=[OrderItem("Mouse", 150.0)])

    # 2. Ejecución
    with uow:
        uow.orders.guardar_orden(orden)
        uow.commit()

    # 3. Comprobaciones
    assert uow.commited is True
    assert "1" in uow.session_data
    assert uow.session_data["1"].cliente == "Aerin"


def test_uow_rollback_automatico_en_caso_de_error() -> None:
    # 1. Preparación
    uow = MemoriaUnitOfWork()
    orden = Order(id="2", cliente="Aerin", items=[OrderItem("Monitor", 3000.0)])

    # 2. Ejecución simulando una falla de sistema
    with pytest.raises(RuntimeError), uow:
        uow.orders.guardar_orden(orden)
        # Simulamos que algo falla antes de hacer commit (ej. se cae la red)
        raise RuntimeError("Falla catastrófica de red")

    # 3. Comprobaciones
    # El UoW debió interceptar el error y limpiar la base de datos para no dejar datos a medias
    assert uow.commited is False
    assert len(uow.session_data) == 0  # La base de datos debe estar vacía
