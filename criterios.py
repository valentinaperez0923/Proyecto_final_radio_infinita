"""Criterios de elección. Todos reciben (cancion, oyente).

- Los PUNTAJES devuelven un número: más alto = mejor.
- Los FILTROS devuelven True/False: si da False, la canción no puede sonar ahora.
"""

from modelo import Cancion, Oyente


def afinidad(cancion: Cancion, oyente: Oyente) -> float:
    """Puntaje: cuántas veces el oyente escuchó entera una canción de este artista."""
    return float(sum(
        1 for e in oyente.escuchas
        if e.completa and e.cancion.artista == cancion.artista
    ))


def energia_objetivo(objetivo: int):
    """Fabrica un puntaje: más puntos cuanto más cerca esté la energía del objetivo."""
    def puntaje(cancion: Cancion, oyente: Oyente) -> float:
        return 10.0 - abs(cancion.energia - objetivo)
    return puntaje


def variedad(ultimas: int):
    """Fabrica un filtro: no deja repetir un artista que sonó en las últimas N escuchas.

    Mira TODAS las escuchas (completas o cortadas), porque una canción
    cortada también sonó.
    """
    if ultimas < 1:
        raise ValueError("ultimas tiene que ser al menos 1")

    def filtro(cancion: Cancion, oyente: Oyente) -> bool:
        recientes = oyente.escuchas[-ultimas:]
        return all(e.cancion.artista != cancion.artista for e in recientes)
    return filtro