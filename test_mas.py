from itertools import islice

import pytest

from modelo import Cancion, Catalogo, Oyente, Pausa
from criterios import afinidad, energia_objetivo, variedad, no_repetir_cancion
from radio import Radio
from catalogo_datos import CATALOGO

A = Cancion(1, "Arranque", "Los Pesos", bpm=125, duracion=180)
B = Cancion(2, "Sprint", "Nadia K", bpm=155, duracion=200)


def nueva_radio(n_pausa=4):
    return Radio(
        CATALOGO,
        puntajes=[afinidad, energia_objetivo(8)],
        filtros=[variedad(2)],
        n_pausa=n_pausa,
    )


def primeros(radio, oyente, n):
    return list(islice(radio.flujo(oyente), n))


# --- Datos inválidos ---

def test_catalogo_vacio_da_error():
    with pytest.raises(ValueError):
        Catalogo(())


def test_catalogo_con_ids_repetidos_da_error():
    otra_con_id_1 = Cancion(1, "Otra", "Otro", bpm=118, duracion=100)
    with pytest.raises(ValueError):
        Catalogo((A, otra_con_id_1))


def test_cancion_con_duracion_cero_da_error():
    with pytest.raises(ValueError):
        Cancion(9, "X", "Y", bpm=118, duracion=0)


def test_no_se_puede_cambiar_una_cancion():
    with pytest.raises(AttributeError):
        A.bpm = 200


def test_no_se_puede_modificar_el_historial_desde_afuera():
    oyente = Oyente("Ana")
    oyente.registrar_escucha(A, completa=True)
    with pytest.raises(AttributeError):
        oyente.escuchas.append("algo")


def test_n_pausa_menor_que_uno_da_error():
    with pytest.raises(ValueError):
        Radio(CATALOGO, [], [], n_pausa=0)


def test_filtros_con_cero_canciones_dan_error():
    with pytest.raises(ValueError):
        variedad(0)
    with pytest.raises(ValueError):
        no_repetir_cancion(0)


def test_pausa_con_duracion_cero_da_error():
    with pytest.raises(ValueError):
        Pausa(0)


# --- Criterios ---

def test_afinidad_solo_cuenta_las_completas():
    oyente = Oyente("Ana")
    oyente.registrar_escucha(A, completa=True)
    oyente.registrar_escucha(A, completa=False)
    assert afinidad(A, oyente.escuchas) == 1


def test_energia_objetivo_da_mas_puntos_cuanto_mas_cerca():
    puntaje = energia_objetivo(8)
    cerca = Cancion(5, "X", "Y", bpm=145, duracion=100)
    lejos = Cancion(6, "Z", "W", bpm=85, duracion=100)
    assert puntaje(cerca, ()) > puntaje(lejos, ())


def test_variedad_deja_pasar_si_no_sono_el_artista():
    oyente = Oyente("Ana")
    oyente.registrar_escucha(A, completa=True)  # Los Pesos
    assert variedad(1)(B, oyente.escuchas) is True  # Nadia K


def test_no_repetir_cancion_bloquea_la_misma_cancion():
    oyente = Oyente("Ana")
    oyente.registrar_escucha(A, completa=True)
    filtro = no_repetir_cancion(5)
    assert filtro(A, oyente.escuchas) is False
    assert filtro(B, oyente.escuchas) is True


def test_empate_gana_el_id_mas_chico():
    # Las dos tienen energía 8 y nadie las escuchó: empatan en puntaje.
    x = Cancion(5, "X", "Uno", bpm=145, duracion=100)
    y = Cancion(2, "Y", "Dos", bpm=148, duracion=100)
    for orden in [(x, y), (y, x)]:
        radio = Radio(Catalogo(orden), [energia_objetivo(8)], [], n_pausa=4)
        assert radio.elegir_siguiente(Oyente("Ana")) == y


def test_la_radio_aprende_de_las_escuchas_completas():
    # Sin historial gana Subida (Los Pesos, energía 8, la de id más chico).
    oyente = Oyente("Ana")
    assert nueva_radio().elegir_siguiente(oyente).id == 3
    # Escucha enteras dos canciones de Nadia K, y después dos de otros
    # artistas para que la variedad deje volver a Nadia K.
    oyente.registrar_escucha(B, completa=True)
    oyente.registrar_escucha(B, completa=True)
    oyente.registrar_escucha(Cancion(99, "X", "Mara Sol", 118, 100), completa=True)
    oyente.registrar_escucha(Cancion(98, "Y", "Río Lento", 118, 100), completa=True)
    assert nueva_radio().elegir_siguiente(oyente).artista == "Nadia K"


# --- Oyente ---

def test_el_historial_tiene_un_limite():
    oyente = Oyente("Ana", memoria=3)
    for _ in range(10):
        oyente.registrar_escucha(A, completa=True)
    assert len(oyente.escuchas) == 3


def test_dos_oyentes_no_se_mezclan():
    radio = nueva_radio()
    ana, beto = Oyente("Ana"), Oyente("Beto")
    ana.registrar_escucha(A, completa=True)
    assert len(ana.escuchas) == 1
    assert len(beto.escuchas) == 0
    # Beto, sin historial, recibe lo mismo que un oyente nuevo.
    assert radio.elegir_siguiente(beto) == radio.elegir_siguiente(Oyente("Carla"))


# --- Flujo ---

def test_mismos_datos_mismo_flujo():
    def correr():
        oyente = Oyente("Ana")
        resultado = []
        for x in islice(nueva_radio().flujo(oyente), 10):
            if isinstance(x, Cancion):
                oyente.registrar_escucha(x, completa=x.energia >= 7)
            resultado.append(x)
        return resultado
    assert correr() == correr()


def test_cambiar_n_pausa_mueve_las_pausas():
    elementos = primeros(nueva_radio(n_pausa=3), Oyente("Ana"), 8)
    posiciones = [i for i, x in enumerate(elementos) if isinstance(x, Pausa)]
    assert posiciones == [3, 7]


def test_el_flujo_no_se_corta():
    # Pedimos muchos elementos: si el flujo terminara, saldrían menos.
    assert len(primeros(nueva_radio(), Oyente("Ana"), 500)) == 500


def test_el_flujo_es_perezoso():
    # Pedir el flujo no calcula nada todavía: recién con next() elige.
    flujo = nueva_radio().flujo(Oyente("Ana"))
    assert isinstance(next(flujo), Cancion)


def test_con_no_repetir_la_radio_no_se_encierra_en_pocas_canciones():
    radio = Radio(
        CATALOGO,
        puntajes=[afinidad, energia_objetivo(8)],
        filtros=[variedad(2), no_repetir_cancion(10)],
        n_pausa=4,
    )
    oyente = Oyente("Ana")
    canciones = []
    # Se recorre el flujo de a uno (sin armar una lista antes), para que cada
    # escucha quede registrada antes de pedir la siguiente canción.
    for x in islice(radio.flujo(oyente), 12):
        if isinstance(x, Cancion):
            oyente.registrar_escucha(x, completa=x.energia >= 7)
            canciones.append(x.id)
    # 10 canciones en 12 elementos (hay 2 pausas), y ninguna se repite.
    assert len(canciones) == 10
    assert len(set(canciones)) == 10