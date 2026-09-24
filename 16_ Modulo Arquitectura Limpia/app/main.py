from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.application.use_cases import CrearOrdenUseCase
from app.infrastructure.unit_of_work import MemoriaUnitOfWork
from app.interface_adapters.presenters import OrderPresenter

# El Adaptador de Entrada (Controlador Web) y el Orquestador de Dependencias


# 1. Esquemas de entrada (Validación HTTP)
class ItemInput(BaseModel):
    nombre: str
    precio: float


class OrderInput(BaseModel):
    id_orden: str
    cliente: str
    items: list[ItemInput]


# 2. Inyeccion de dependencias global

# Instanciamos la Infraestructura
uow = MemoriaUnitOfWork()
# Instanciamos la Aplicación inyectándole la Infraestructura
caso_de_uso = CrearOrdenUseCase(uow=uow)

# 3. Controlador web (Capa 4: Infraestructura / Capa 3: Controladores)
app = FastAPI(title="Arquitectura Limpia")


@app.post("/ordenes/", response_model=dict)
def crear_orden_endpoint(datos: OrderInput) -> dict:
    try:
        # Extraemos los datos del framework HTTP
        items_dict = [{"nombre": i.nombre, "precio": i.precio} for i in datos.items]

        # Ejecutamos el Caso de Uso (Capa 2)
        orden_creada = caso_de_uso.ejecutar(
            id_orden=datos.id_orden, cliente=datos.cliente, items_data=items_dict
        )

        # Usamos el Presentador (Capa 3) para formatear la respuesta
        return OrderPresenter.to_api_dict(orden_creada)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
