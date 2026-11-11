"""Criterios de elección. Todos son funciones puras que reciben (cancion, escuchas).

- Los PUNTAJES devuelven un número: más alto = mejor.
- Los FILTROS devuelven True/False: si da False, la canción no puede sonar ahora.

`escuchas` es una tupla (no se puede modificar), así que con los mismos
datos cada criterio devuelve siempre lo mismo.
"""

from typing import Callable

from modelo import Cancion, Escucha

# Nombres cortos para los tipos, así el resto del programa se lee mejor.
Escuchas = tuple[Escucha, ...]
Puntaje = Callable[[Cancion, Escuchas], float]
Filtro = Callable[[Cancion, Escuchas], bool]


# ---------- PUNTAJES ----------

def afinidad(cancion: Cancion, escuchas: Escuchas) -> float:
    """Cuántas veces se escuchó COMPLETA una canción de este artista."""
    cantidad = 0
    for e in escuchas:
        if e.completa and e.cancion.artista == cancion.artista:
            cantidad += 1
    return float(cantidad)


def energia_objetivo(objetivo: int) -> Puntaje:
    """Crea un puntaje: más puntos cuanto más cerca esté la energía del objetivo."""
    def puntaje(cancion: Cancion, escuchas: Escuchas) -> float:
        return 10.0 - abs(cancion.energia - objetivo)
    return puntaje


# ---------- FILTROS ----------

def _sin_repetir(que_comparar, ultimas: int) -> Filtro:
    """Base de los dos filtros de abajo.

    `que_comparar` es una función que, dada una canción, devuelve el dato
    a comparar (su artista, su id, etc.). El filtro rechaza la canción si
    ese dato ya apareció en las últimas N escuchas.
    """
    if ultimas < 1:
        raise ValueError("ultimas tiene que ser al menos 1")

    def filtro(cancion: Cancion, escuchas: Escuchas) -> bool:
        recientes = escuchas[-ultimas:]
        for e in recientes:
            if que_comparar(e.cancion) == que_comparar(cancion):
                return False
        return True
    return filtro


def variedad(ultimas: int) -> Filtro:
    """No deja repetir un ARTISTA que sonó en las últimas N escuchas."""
    return _sin_repetir(lambda c: c.artista, ultimas)


def no_repetir_cancion(ultimas: int) -> Filtro:
    """No deja repetir la misma CANCIÓN en las últimas N escuchas."""
    return _sin_repetir(lambda c: c.id, ultimas)