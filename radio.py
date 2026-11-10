"""La radio: elige la próxima canción y arma el flujo infinito con pausas."""

from typing import Iterator

from modelo import Catalogo, Oyente, Cancion, Pausa, Emitible


def elegir_siguiente(canciones, escuchas, puntajes, filtros) -> Cancion:
    """Función pura: con los mismos datos devuelve siempre la misma canción."""
    # 1. Filtros: quedan solo las canciones que pasan todos.
    candidatas = [
        c for c in canciones
        if all(filtro(c, escuchas) for filtro in filtros)
    ]
    # 2. Si no queda ninguna, la que hace más tiempo que no suena.
    if not candidatas:
        return la_que_hace_mas_que_no_suena(canciones, escuchas)
    # 3. Gana la de mayor puntaje. Si empatan, la de id más chico.
    return max(
        candidatas,
        key=lambda c: (sum(p(c, escuchas) for p in puntajes), -c.id),
    )


def la_que_hace_mas_que_no_suena(canciones, escuchas) -> Cancion:
    """Función pura: la canción que sonó hace más tiempo (o nunca sonó)."""
    ultima_vez = {}
    for posicion, escucha in enumerate(escuchas):
        ultima_vez[escucha.cancion.id] = posicion
    # Las que nunca sonaron tienen -1, así que van primero. Empate: id más chico.
    return min(canciones, key=lambda c: (ultima_vez.get(c.id, -1), c.id))


class Radio:
    def __init__(self, catalogo: Catalogo, puntajes, filtros,
                 n_pausa: int, duracion_pausa: float = 60):
        if n_pausa < 1:
            raise ValueError("n_pausa tiene que ser al menos 1")
        self.catalogo = catalogo
        self.puntajes = tuple(puntajes)
        self.filtros = tuple(filtros)
        self.n_pausa = n_pausa
        self.pausa = Pausa(duracion_pausa)

    def elegir_siguiente(self, oyente: Oyente) -> Cancion:
        return elegir_siguiente(
            self.catalogo.canciones, oyente.escuchas, self.puntajes, self.filtros
        )

    def flujo(self, oyente: Oyente) -> Iterator[Emitible]:
        """Entrega de a un elemento, para siempre. Cada n_pausa canciones, una Pausa.

        Quien consume el flujo tiene que registrar cada escucha en el oyente
        antes de pedir el siguiente elemento: así la radio aprende.
        """
        contador = 0
        while True:
            if contador == self.n_pausa:
                yield self.pausa
                contador = 0
            else:
                yield self.elegir_siguiente(oyente)
                contador += 1