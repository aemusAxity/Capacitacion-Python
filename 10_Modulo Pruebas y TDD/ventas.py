from datetime import datetime, timezone


def aplicar_descuento(precio: float, porcentaje_descuento: float) -> float:

    if porcentaje_descuento > 70.0:
        raise ValueError("El porcentaje no puede ser mayor a 70")

    if porcentaje_descuento < 0.0:
        raise ValueError("El porcentaje no puede ser negativo")

    monto_descuento = precio * (porcentaje_descuento / 100)
    precio_final = precio - monto_descuento

    return max(0.0, precio_final)


def viernes_oferta() -> bool:
    hoy = datetime.now(timezone.utc)
    # En Python, el 4 significa Viernes (Lunes=0, Martes=1...)
    return hoy.weekday() == 4


# Compras mayores a $50 tienen envio gratis cuando es viernes
def envio_gratis(monto_compra: float) -> bool:
    return bool(monto_compra >= 50.0 and viernes_oferta())
