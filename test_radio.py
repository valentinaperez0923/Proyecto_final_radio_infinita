from itertools import islice

import pytest

from modelo import Cancion, Catalogo, Oyente, Pausa
from criterios import afinidad, energia_objetivo, variedad
from radio import Radio

A = Cancion(1, "Arranque", "Los Pesos", bpm=125, duracion=180)
B = Cancion(2, "Sprint", "Nadia K", bpm=155, duracion=200)
C = Cancion(3, "Subida", "Los Pesos", bpm=145, duracion=210)


def nueva_radio(canciones=(A, B, C), n_pausa=2):
    return Radio(
        Catalogo(canciones),
        puntajes=[afinidad, energia_objetivo(8)],
        filtros=[variedad(1)],
        n_pausa=n_pausa,
    )


def test_no_se_puede_crear_cancion_con_bpm_invalidos():
    with pytest.raises(ValueError):
        Cancion(9, "X", "Y", bpm=0, duracion=100)


def test_la_energia_se_calcula_con_los_bpm():
    assert Cancion(9, "X", "Y", bpm=70, duracion=100).energia == 1
    assert Cancion(9, "X", "Y", bpm=145, duracion=100).energia == 8
    assert Cancion(9, "X", "Y", bpm=200, duracion=100).energia == 10


def test_sin_historial_gana_la_energia_mas_cercana():
    assert nueva_radio().elegir_siguiente(Oyente("Ana")) == C


def test_una_cancion_salteada_cuenta_para_la_variedad():
    oyente = Oyente("Ana")
    oyente.registrar_escucha(C, completa=False)  # la cortó
    # Los Pesos acaba de sonar, así que quedan afuera A y C.
    assert nueva_radio().elegir_siguiente(oyente) == B


def test_si_el_filtro_descarta_todo_suena_la_que_hace_mas_que_no_suena():
    oyente = Oyente("Ana")
    oyente.registrar_escucha(C, completa=True)
    # Solo hay canciones de Los Pesos: el filtro las descarta a las dos.
    # A nunca sonó, así que es la que hace más tiempo que no suena.
    assert nueva_radio(canciones=(A, C)).elegir_siguiente(oyente) == A


def test_el_orden_del_catalogo_no_cambia_el_resultado():
    assert nueva_radio(canciones=(C, B, A)).elegir_siguiente(Oyente("Ana")) == C


def test_hay_una_pausa_cada_n_canciones():
    primeros = list(islice(nueva_radio(n_pausa=2).flujo(Oyente("Ana")), 6))
    tipos = [type(x) for x in primeros]
    assert tipos == [Cancion, Cancion, Pausa, Cancion, Cancion, Pausa]