from app.domain.events import OrderCreated
from app.domain.order import Order, OrderItem
from app.interface_adapters.presenters import OrderPresenter


def test_order_presenter_formatea_correctamente() -> None:
    # 1. Preparación (Arrange)
    # Creamos una Entidad de Dominio real con datos específicos
    item = OrderItem(
        nombre="Teclado", precio=1200.555
    )  # Decimal largo para probar el redondeo
    orden = Order(id="777", cliente="Max", items=[item])
    # Forzamos un evento extra para probar el contador
    orden.events.append(OrderCreated(order_id="777"))

    # 2. Ejecución (Act)
    # Pasamos la Entidad por el Presentador
    resultado_api = OrderPresenter.to_api_dict(orden)

    # 3. Comprobaciones (Assert)
    # Validamos las transformaciones específicas de la capa de interfaz
    assert resultado_api["id"] == "777"
    assert resultado_api["cliente"] == "MAX"  # Debe aplicar uppercase
    assert resultado_api["total"] == 1200.56  # Debe redondear a 2 decimales
    assert resultado_api["estado"] == "PENDIENTE"
    # Debe haber 2 eventos (el automático del __post_init__ y el manual)
    assert resultado_api["eventos_generados"] == 2
