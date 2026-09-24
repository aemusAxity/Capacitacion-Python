from typing import Any

from app.domain.order import Order

# PRESENTADOR (Capa 3: Interface Adapters).
# Toma la Entidad 'Order' y la formatea para la vista (API Web).
# Formatea la respuesta del Caso de Uso hacia el exterior.


class OrderPresenter:
    @staticmethod
    def to_api_dict(order: Order) -> dict[str, Any]:
        return {
            "id": order.id,
            "cliente": order.cliente.upper(),  # Ejemplo de formato de vista
            "total": round(order.total, 2),
            "estado": order.status,
            "eventos_generados": len(order.events),
        }
