import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from pydantic import BaseModel, Field, ValidationError

# 1. Modelo Pydantic de validacion


class OrderIn(BaseModel):
    producto: str = Field(..., min_length=3, description="Nombre del producto")
    cantidad: int = Field(..., gt=0, description="Debe ser mayor a 0")
    precio_unitario: float = Field(..., ge=0, description="No puede ser negativo")
    cliente: str


class OrderOut(BaseModel):
    id_orden: str
    producto: str
    total: float
    fecha: datetime


# 2. Entidad de negocio (dataclass)


@dataclass
class Order:
    producto: str
    cantidad: int
    precio_unitario: float
    cliente: str

    id_orden: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    fecha: datetime = field(default_factory=datetime.now)

    @property
    def total(self) -> float:
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"Orden [{self.id_orden}] - {self.producto} x{self.cantidad} (${self.total})"

    def __eq__(self, otra_orden):
        if not isinstance(otra_orden, Order):
            return False
        return (
            self.cliente == otra_orden.cliente and self.producto == otra_orden.producto
        )


# 3. Lectura de JSON
if __name__ == "__main__":
    # 1. Leyendo archivo JSON
    print("PASO 1: Leyendo petición desde el archivo 'pedido.json'...")
    try:
        with open("pedidos.json", "r", encoding="utf-8") as archivo:
            # json.load convierte el texto del archivo a un diccionario de Python
            peticion_json = json.load(archivo)
            print(f"Datos crudos leídos: {peticion_json}\n")

        # 2. Validar con pydantic
        print("PASO 2: Pydantic revisa y limpia los datos...")
        datos_limpios = OrderIn(**peticion_json)
        diccionario_limpio = datos_limpios.model_dump()
        print("¡Datos aprobados!\n")

        # 3. Creación de entidad dataclass
        print("PASO 3: Construimos nuestra Entidad Interna...")
        orden_interna = Order(**diccionario_limpio)
        print(f"Visión interna: {orden_interna}\n")

        # 4. Preparacion de la respuesta
        print("PASO 4: Generando el ticket de salida (OrderOut)...")
        ticket_salida = OrderOut(
            id_orden=orden_interna.id_orden,
            producto=orden_interna.producto,
            total=orden_interna.total,
            fecha=orden_interna.fecha,
        )

        # Imprimimos el resultado como texto plano
        print("Ticket generado:")
        print("-" * 30)
        print(f"ID del Pedido : {ticket_salida.id_orden}")
        print(f"Producto      : {ticket_salida.producto}")
        print(f"Total a Pagar : ${ticket_salida.total}")
        print(f"Fecha         : {ticket_salida.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 30)

    except FileNotFoundError:
        print(
            "Error: No se encontró el archivo 'pedido.json'. Asegúrate de crearlo en esta carpeta."
        )
    except json.JSONDecodeError:
        print("Error: El archivo 'pedido.json' no tiene un formato válido.")
    except ValidationError as e:
        print("\nALERTA: El JSON tiene datos inválidos según nuestras reglas.")
        print(e)
