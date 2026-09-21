from auth import verificar_token
from db_temporal import OrderDB, get_db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

# Aplicamos la protección JWT a todo el router
router = APIRouter(
    prefix="/orders", tags=["Órdenes"], dependencies=[Depends(verificar_token)]
)


# Esquemas Pydantic
class OrderCreate(BaseModel):
    producto: str
    cantidad: int


class OrderResponse(OrderCreate):
    id: int


@router.post("/", response_model=OrderResponse)
def crear_orden(orden: OrderCreate, db: Session = Depends(get_db)):  # noqa: B008
    nueva_orden = OrderDB(producto=orden.producto, cantidad=orden.cantidad)
    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)
    return nueva_orden


@router.get("/", response_model=list[OrderResponse])
def leer_ordenes(db: Session = Depends(get_db)):  # noqa: B008
    return db.execute(select(OrderDB)).scalars().all()
