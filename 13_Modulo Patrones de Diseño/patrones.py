import time
from collections.abc import Callable
from typing import Any, Protocol


# 1. Patron Strategy (Para calcular precios)
# Creamos el Protocolo
class EstrategiaDescuento(Protocol):
    def aplicar(self, precio: float) -> float: ...


# Clases que "implementan" (cumplen con) el Protocolo
class SinDescuento:
    def aplicar(self, precio: float) -> float:
        return precio


class DescuentoBlackFriday:
    def aplicar(self, precio: float) -> float:
        return precio * 0.50


class DescuentoVIP:
    def aplicar(self, precio: float) -> float:
        return precio * 0.80


# El Carrito el que usa la estrategia
class CarritoCompras:
    # Estrategia es una varaible que cumple con protocol, se deja por default sin descuento
    def __init__(self, estrategia: EstrategiaDescuento = SinDescuento()):  # noqa: B008
        self.total: float = 0.0
        # Inyectamos el objeto de la estrategia
        self.estrategia = estrategia

    def agregar_item(self, precio: float) -> None:
        self.total += precio

    def calcular_total(self) -> float:
        # Llamamos explícitamente al método ".aplicar()" del objeto estrategia
        return self.estrategia.aplicar(self.total)


# 2. Patron Decorator (caché)


# Decorador clásico que guarda resultados previos en memoria
def cache_simple(funcion: Callable) -> Callable:
    memoria_cache: dict[tuple, Any] = {}

    def envoltura(*args):
        # Si ya calculamos esto antes, devolvemos lo guardado
        if args in memoria_cache:
            print(f"Usando Caché para los argumentos: {args}")
            return memoria_cache[args]

        # Si es nuevo, calculamos, guardamos y devolvemos
        print(f"Calculando resultado nuevo para: {args}")
        resultado = funcion(*args)
        memoria_cache[args] = resultado
        return resultado

    return envoltura


@cache_simple
# Simula ir a internet o hacer matemáticas pesadas
def operacion_muy_lenta(numero: int) -> int:
    time.sleep(1)  # Tarda a propósito
    return numero * 100


# 3. Patron Adapter (proveedor externo)


# Nuestro sistema habla en JSON
class MiSistema(Protocol):
    def enviar_orden(self, datos_json: dict) -> str: ...


# El código del proveedor externo
# No podemos modificar esto porque es de otra empresa.
class ProveedorExternoViejo:
    def send_xml_request(self, xml_data: str) -> str:
        return f"Procesado XML: {xml_data}"


# El Adaptador (Traduce de JSON a XML)
class AdaptadorProveedor(MiSistema):
    def __init__(self, proveedor_viejo: ProveedorExternoViejo):
        self.proveedor_viejo = proveedor_viejo

    def enviar_orden(self, datos_json: dict) -> str:
        # 1. Traducimos el idioma (JSON a XML falso)
        xml_falso = f"<orden><id>{datos_json.get('id', 0)}</id></orden>"
        # 2. Usamos la herramienta vieja
        respuesta = self.proveedor_viejo.send_xml_request(xml_falso)
        return respuesta
