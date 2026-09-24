import pytest
from app.domain.events import OrderCreated
from app.domain.order import Order, OrderItem


def test_order_creacion_exitosa_y_registro_de_evento() -> None:
    # Preparación
    items = [OrderItem(nombre="Laptop", precio=15000.0)]

    # Ejecución
    orden = Order(id="100", cliente="Melody", items=items)

    # Comprobaciones de negocio
    assert orden.total == 15000.0

    # Comprobación de Arquitectura Limpia (Eventos)
    assert len(orden.events) == 1
    assert isinstance(orden.events[0], OrderCreated)
    assert orden.events[0].order_id == "100"


def test_order_falla_sin_items() -> None:
    with pytest.raises(ValueError, match="al menos un artículo"):
        Order(id="101", cliente="Pedro", items=[])
