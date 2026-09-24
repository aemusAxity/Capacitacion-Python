from app.application.ports import OrderRepository
from app.domain.order import Order


# Adaptador de salida (Infraestructura)
# Esta clase si guarda e implementa la interfaz OrderRepository
class BaseDeDatosEnMemoria(OrderRepository):
    def __init__(self) -> None:
        # Simulamos una tabla de base de datos usando un diccionario de Python
        self.tabla_ordenes: dict[str, Order] = {}

    def guardar_orden(self, orden: Order) -> None:
        self.tabla_ordenes[orden.id] = orden
        print(f"[BD] Orden {orden.id} guardada exitosamente.")
