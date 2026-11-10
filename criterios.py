"""Criterios de elección. Todos son funciones puras que reciben (cancion, escuchas).

`escuchas` es una tupla: no se puede modificar, así que con los mismos
datos cada criterio devuelve siempre lo mismo.

- Los PUNTAJES devuelven un número: más alto = mejor.
- Los FILTROS devuelven True/False: si da False, la canción no puede sonar ahora.
"""

from modelo import Cancion, Escucha

Escuchas = tuple[Escucha, ...]


def afinidad(cancion: Cancion, escuchas: Escuchas) -> float:
    """Puntaje: cuántas veces se escuchó entera una canción de este artista."""
    return float(sum(
        1 for e in escuchas
        if e.completa and e.cancion.artista == cancion.artista
    ))


def energia_objetivo(objetivo: int):
    """Fabrica un puntaje: más puntos cuanto más cerca esté la energía del objetivo."""
    def puntaje(cancion: Cancion, escuchas: Escuchas) -> float:
        return 10.0 - abs(cancion.energia - objetivo)
    return puntaje


def variedad(ultimas: int):
    """Fabrica un filtro: no deja repetir un ARTISTA que sonó en las últimas N escuchas.

    Mira todas las escuchas (completas o cortadas), porque una canción
    cortada también sonó.
    """
    if ultimas < 1:
        raise ValueError("ultimas tiene que ser al menos 1")

    def filtro(cancion: Cancion, escuchas: Escuchas) -> bool:
        return all(e.cancion.artista != cancion.artista for e in escuchas[-ultimas:])
    return filtro


def no_repetir_cancion(ultimas: int):
    """Fabrica un filtro: no deja repetir la misma CANCIÓN en las últimas N escuchas."""
    if ultimas < 1:
        raise ValueError("ultimas tiene que ser al menos 1")

    def filtro(cancion: Cancion, escuchas: Escuchas) -> bool:
        return all(e.cancion.id != cancion.id for e in escuchas[-ultimas:])
    return filtro