from app.domain.order import Order, OrderItem
from app.infrastructure.repositories import BaseDeDatosEnMemoria


def test_bd_en_memoria_guarda_orden() -> None:
    # 1. Preparamos la Base de Datos
    repo = BaseDeDatosEnMemoria()

    # 2. Creamos una orden de prueba
    item = OrderItem(nombre="Monitor", precio=3500.0)
    orden = Order(id="340", cliente="Paul", items=[item])

    # 3. Ejecutamos el guardado
    repo.guardar_orden(orden)

    # 4. Verificamos que realmente se guardó en el diccionario interno
    assert "340" in repo.tabla_ordenes
    assert repo.tabla_ordenes["340"].cliente == "Paul"
