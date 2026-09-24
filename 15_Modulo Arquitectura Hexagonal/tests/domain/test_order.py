import pytest
from app.domain.order import Order, OrderItem


def test_orden_calcula_el_total_correctamente() -> None:
    # 1. Preparamos los datos
    item1 = OrderItem(nombre="Laptop", precio=15000.0)
    item2 = OrderItem(nombre="Teclado", precio=500.0)

    # 2. Ejecutamos (Creamos la orden)
    orden = Order(id="001", cliente="Aerin", items=[item1, item2])

    # 3. Verificamos (Debe sumar 15500 y estar PENDIENTE)
    assert orden.total == 15500.0
    assert orden.status == "PENDIENTE"


def test_orden_sin_items_lanza_error() -> None:
    # Verificamos que el Rey defienda su regla de negocio
    with pytest.raises(ValueError, match="al menos un artículo"):
        Order(id="002", cliente="Saul", items=[])
