"""Los datos de la radio: canciones, pausas, escuchas, catálogo y oyente."""

from dataclasses import dataclass # armar clases sin tener que escribir el init, repr, eq, etc.
from collections import deque # una lista con tamaño máximo, que descarta los elementos más viejos cuando se agregan nuevos. Sirve para guardar el historial de escuchas de un oyente.
from typing import Protocol # sirve para definir qué métodos y propiedades tiene que tener una clase para poder usarla en un contexto determinado. Es como una interfaz en otros lenguajes.


class Emitible(Protocol):
    """Interfaz: todo lo que puede salir por la radio tiene que tener una duracion (una canción o una pausa)."""

    @property   # indica que lo de abajo es una propiedad, no un método. Se puede acceder como si fuera un atributo, pero se calcula al momento de acceder.
    def duracion(self) -> float: ... # para poder salir por la radio, tiene que tener una duracion y ser un float. El ... indica que aca no va nada mas, solo el aviso


@dataclass(frozen=True) # frozen=True hace que la clase sea inmutable, es decir, que no se puedan cambiar los atributos después de crear una instancia.
class Cancion:
    id: int
    titulo: str
    artista: str
    bpm: int          # pulsaciones por minuto (el ritmo)
    duracion: float   # en segundos

    def __post_init__(self):    # despues de definir los atributos, se ejecuta este método para validar los valores. Si no se cumplen, lanza error y no se crea la instancia.
        if not 40 <= self.bpm <= 250:
            raise ValueError("Los bpm tienen que estar entre 40 y 250")
        if self.duracion <= 0:
            raise ValueError("La duración tiene que ser mayor que 0")

    @property # permite usar un método como si fuera un dato. (cancion.energia y no cancion.energia())
    def energia(self) -> int:
        """La energía (1 a 10) se calcula a partir de los bpm, no se guarda.

        Cada 10 bpm por encima de 60 suma 1 de energía:
        70 bpm -> 1, 100 bpm -> 4, 140 bpm -> 8, 160 bpm o más -> 10.
        """
        return min(10, max(1, (self.bpm - 60) // 10))


@dataclass(frozen=True) 
class Pausa:
    duracion: float   # en segundos. Cumple con Emitible porque tiene duracion
    def __post_init__(self):
        if self.duracion <= 0:
            raise ValueError("La duración de la pausa tiene que ser mayor que 0")

@dataclass(frozen=True)
class Escucha:
    """Lo que pasó cuando sonó una canción: si se escuchó entera o no."""
    cancion: Cancion
    completa: bool


@dataclass(frozen=True)
class Catalogo:
    """Las canciones disponibles. Se arma una vez y es el mismo para todos los oyentes."""
    canciones: tuple[Cancion, ...] # un casillero con muchas canciones, en una tupla. Una tupla es una lista que no se puede modificar. Los tres puntos significan “cualquier cantidad”.

    def __post_init__(self): # despues de definir los atributos, se ejecuta este metodo para validar los valores.
        if not self.canciones:
            raise ValueError("El catálogo no puede estar vacío")
        ids = [c.id for c in self.canciones] # arma una lista con los ids de todas las canciones
        if len(ids) != len(set(ids)):       # set es una bolsa que no acepta repetidos. Si la bolsa tiene menos elementos que la lista, es que había números repetidos.
            raise ValueError("Hay canciones con el mismo id")


class Oyente:
    """La única pieza que cambia: va guardando todo lo que escuchó."""

    def __init__(self, nombre: str, memoria: int = 100):
        if memoria < 1:
            raise ValueError("La memoria tiene que ser al menos 1")
        self.nombre = nombre
        self._escuchas: deque[Escucha] = deque(maxlen=memoria) 


    def registrar_escucha(self, cancion: Cancion, completa: bool) -> None:  # recibe la cancion y si se escucho completa. El -> None dice que no devuelve nada, solo anota.
        self._escuchas.append(Escucha(cancion, completa))       # Crea un objeto Escucha y lo agrega a la lista de escuchas del oyente.

    @property       # se va a leer como atributo
    def escuchas(self) -> tuple[Escucha, ...]:  # Define como se leen las escuchas. El -> tuple[Escucha, ...] dice que devuelve una tupla de escuchas, y los tres puntos significan que puede tener cualquier cantidad.
        # Devuelve una copia que no se puede modificar: los criterios solo leen.
        return tuple(self._escuchas) 