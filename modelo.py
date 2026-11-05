"""Los datos de la radio: canciones, pausas, escuchas, catálogo y oyente."""

from dataclasses import dataclass
from typing import Protocol


class Emitible(Protocol):
    """Interfaz: todo lo que puede salir por la radio (una canción o una pausa)."""

    @property
    def duracion(self) -> float: ...


@dataclass(frozen=True)
class Cancion:
    id: int
    titulo: str
    artista: str
    energia: int      # de 1 a 10
    duracion: float   # en segundos

    def __post_init__(self):
        if not 1 <= self.energia <= 10:
            raise ValueError("La energía tiene que estar entre 1 y 10")
        if self.duracion <= 0:
            raise ValueError("La duración tiene que ser mayor que 0")


@dataclass(frozen=True)
class Pausa:
    duracion: float   # en segundos


@dataclass(frozen=True)
class Escucha:
    """Lo que pasó cuando sonó una canción: si se escuchó entera o no."""
    cancion: Cancion
    completa: bool


@dataclass(frozen=True)
class Catalogo:
    """Las canciones disponibles. Se arma una vez y es el mismo para todos los oyentes."""
    canciones: tuple[Cancion, ...]

    def __post_init__(self):
        if not self.canciones:
            raise ValueError("El catálogo no puede estar vacío")
        ids = [c.id for c in self.canciones]
        if len(ids) != len(set(ids)):
            raise ValueError("Hay canciones con el mismo id")


class Oyente:
    """La única pieza que cambia: va guardando todo lo que escuchó."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self._escuchas: list[Escucha] = []

    def registrar_escucha(self, cancion: Cancion, completa: bool) -> None:
        self._escuchas.append(Escucha(cancion, completa))

    @property
    def escuchas(self) -> tuple[Escucha, ...]:
        # Devuelve una copia que no se puede modificar: los criterios solo leen.
        return tuple(self._escuchas)