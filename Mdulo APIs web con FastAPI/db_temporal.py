from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# DB Temporal
engine = create_engine(
    "sqlite:///db_temporal.sqlite", connect_args={"check_same_thread": False}
)


class Base(DeclarativeBase):
    pass


class OrderDB(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    producto: Mapped[str] = mapped_column()
    cantidad: Mapped[int] = mapped_column()


# Creamos las tablas
Base.metadata.create_all(engine)


# Inyección de dependencias para dar acceso a la BD a los routers
def get_db():
    with Session(engine) as session:
        yield session
