import time

from patrones import (
    AdaptadorProveedor,
    CarritoCompras,
    DescuentoBlackFriday,
    DescuentoVIP,
    ProveedorExternoViejo,
    operacion_muy_lenta,
)

# Prueba Strategy


def test_strategy_sin_descuento():
    carrito = CarritoCompras()  # Por defecto es sin descuento
    carrito.agregar_item(100.0)
    assert carrito.calcular_total() == 100.0


def test_strategy_black_friday():
    # Inyectamos la estrategia dinámicamente
    carrito = CarritoCompras(estrategia=DescuentoBlackFriday())
    carrito.agregar_item(100.0)
    assert carrito.calcular_total() == 50.0


def test_strategy_desc_VIP():
    carrito = CarritoCompras(estrategia=DescuentoVIP())
    carrito.agregar_item(100.0)
    assert carrito.calcular_total() == 80.0


# Prueba decorator


def test_decorator_cache():
    # Primera llamada (debe tardar 1 segundo)
    inicio = time.perf_counter()
    resultado1 = operacion_muy_lenta(5)
    tiempo1 = time.perf_counter() - inicio

    # Segunda llamada con el MISMO argumento (debe ser instantánea gracias al Caché)
    inicio = time.perf_counter()
    resultado2 = operacion_muy_lenta(5)
    tiempo2 = time.perf_counter() - inicio

    assert resultado1 == 500
    assert resultado2 == 500
    assert tiempo1 >= 1.0  # Tardó al menos 1 seg
    assert tiempo2 < 0.1  # Fue instantáneo (<0.1s)


# Prueba Adapter


def test_adapter_traduccion():
    # Tenemos la herramienta vieja (de la otra empresa)
    herramienta_vieja = ProveedorExternoViejo()

    # Creamos el adaptador y le conectamos la herramienta vieja
    adaptador = AdaptadorProveedor(proveedor_viejo=herramienta_vieja)

    # Nuestro sistema envía un JSON moderno
    mi_json = {"id": 12345}

    # El adaptador lo recibe, lo traduce, y devuelve la respuesta
    resultado = adaptador.enviar_orden(mi_json)

    assert resultado == "Procesado XML: <orden><id>12345</id></orden>"
