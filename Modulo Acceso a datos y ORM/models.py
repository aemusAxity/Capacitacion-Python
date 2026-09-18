from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Clase base de la que heredarán todos nuestros modelos
class Base(DeclarativeBase):
    pass


# 1. Tabla: Usuarios


class User(Base):
    __tablename__ = "users"  # Nombre real en la BD

    # Columnas
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)

    # Relación: Un usuario puede tener múltiples órdenes
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, nombre='{self.nombre}')>"


# 2. Tabla Ordnenes (pedidos)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Llave foránea que conecta con la tabla users
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    estado: Mapped[str] = mapped_column(String(20), default="PENDIENTE")

    # Relaciones (Navegación bidireccional)
    user: Mapped["User"] = relationship(back_populates="orders")
    # Una orden tiene múltiples ítems (productos)
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, estado='{self.estado}')>"


# 3. Tabla Detalles de la orden


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    producto: Mapped[str] = mapped_column(String(100))
    cantidad: Mapped[int] = mapped_column()
    precio_unitario: Mapped[float] = mapped_column()

    # Relación hacia arriba (A qué orden pertenece)
    order: Mapped["Order"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"<OrderItem(producto='{self.producto}', cant={self.cantidad})>"
