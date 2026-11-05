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
    bpm: int          # pulsaciones por minuto (el ritmo)
    duracion: float   # en segundos

    def __post_init__(self):
        if not 40 <= self.bpm <= 250:
            raise ValueError("Los bpm tienen que estar entre 40 y 250")
        if self.duracion <= 0:
            raise ValueError("La duración tiene que ser mayor que 0")

    @property
    def energia(self) -> int:
        """La energía (1 a 10) se calcula a partir de los bpm, no se guarda.

        Cada 10 bpm por encima de 60 suma 1 de energía:
        70 bpm -> 1, 100 bpm -> 4, 140 bpm -> 8, 160 bpm o más -> 10.
        """
        return min(10, max(1, (self.bpm - 60) // 10))


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