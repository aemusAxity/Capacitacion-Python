import datetime
from unittest.mock import patch

import pytest
from hypothesis import given
from hypothesis import strategies as st
from ventas import aplicar_descuento, envio_gratis, viernes_oferta


def test_descuento_normal():
    resultado = aplicar_descuento(100.0, 20.0)
    assert resultado == 80.0


def test_descuento_mitad():
    resultado = aplicar_descuento(50.0, 50.0)
    assert resultado == 25.0


def test_descuento_mayor_a_70_lanza_error():
    # Usamos pytest.raises para decirle a la prueba que ESTAMOS ESPERANDO que el código explote.
    with pytest.raises(ValueError, match="El porcentaje no puede ser mayor a 70"):
        aplicar_descuento(100.0, 150.0)


def test_descuento_menor_a_0_lanza_error():
    with pytest.raises(ValueError, match="El porcentaje no puede ser negativo"):
        aplicar_descuento(100.0, -10.0)


def test_no_envio_gratis_los_viernes():
    resultado = envio_gratis(100.0)
    assert resultado == False


# Testing (hypothesis)


# @given es el generador. Le pedimos a Hypothesis que genere:
# 1. Un precio aleatorio (flotante) entre 0.0 y 1,000,000.0
# 2. Un descuento aleatorio (flotante) entre 0.0 y 70.0
@given(
    precio_aleatorio=st.floats(min_value=0.0, max_value=1000000.0),
    descuento_aleatorio=st.floats(min_value=0.0, max_value=70.0),
)
def test_propiedades_del_descuento(precio_aleatorio, descuento_aleatorio):
    """
    Hypothesis correrá esta función cientos de veces con números raros como:
    (0.00001, 99.999), (500.5, 0.0), (1000000.0, 100.0), etc.
    """

    # 1. Ejecutamos la función con los datos locos
    resultado = aplicar_descuento(precio_aleatorio, descuento_aleatorio)

    # 2. Comprobamos las Propiedades Universales

    # Propiedad A: Nunca debe quedar en números rojos
    assert resultado >= 0.0

    # Propiedad B: El precio con descuento jamás debe ser más caro que el original
    assert resultado <= precio_aleatorio


# Mocks
# Secuestramos ESPECÍFICAMENTE a 'datetime' DENTRO de tu archivo 'ventas'
@patch("ventas.datetime")
def test_viernes_con_mock(mock_datetime):
    # Creamos un "viernes" falso (24 de Noviembre de 2023)
    viernes_falso = datetime.datetime(2023, 11, 24, tzinfo=datetime.timezone.utc)

    # Le decimos al Mock: "Cuando mi código te pida el .now(), dale el viernes falso"
    mock_datetime.now.return_value = viernes_falso

    # Corremos nuestra función REAL.
    # Nuestra función entrará a la línea "hoy = datetime.now()".
    # Y el Mock le entregará nuestro viernes falso.
    resultado = viernes_oferta()
    assert resultado == True


@patch("ventas.datetime")
def test_viernes_envio_mock(mock_datetime):
    # Creamos un "viernes" falso (24 de Noviembre de 2023)
    viernes_falso = datetime.datetime(2023, 11, 24, tzinfo=datetime.timezone.utc)

    mock_datetime.now.return_value = viernes_falso
    resultado = envio_gratis(100)
    assert resultado == True


@patch("ventas.datetime")
def test_lunes_con_mock(mock_datetime):
    # Creamos un "lunes" falso
    lunes_falso = datetime.datetime(2023, 11, 20, tzinfo=datetime.timezone.utc)

    # Engañamos al .now()
    mock_datetime.now.return_value = lunes_falso

    resultado = viernes_oferta()
    assert resultado == False
