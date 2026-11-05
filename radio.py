"""La radio: elige la próxima canción y arma el flujo infinito con pausas."""

from typing import Iterator

from modelo import Catalogo, Oyente, Cancion, Pausa, Emitible


class Radio:
    def __init__(self, catalogo: Catalogo, puntajes, filtros,
                 n_pausa: int, duracion_pausa: float = 60):
        if n_pausa < 1:
            raise ValueError("n_pausa tiene que ser al menos 1")
        self.catalogo = catalogo
        self.puntajes = list(puntajes)
        self.filtros = list(filtros)
        self.n_pausa = n_pausa
        self.duracion_pausa = duracion_pausa

    def elegir_siguiente(self, oyente: Oyente) -> Cancion:
        # 1. Filtros: quedan solo las canciones que pasan todos.
        candidatas = [
            c for c in self.catalogo.canciones
            if all(filtro(c, oyente) for filtro in self.filtros)
        ]
        # 2. Si no queda ninguna, la que hace más tiempo que no suena.
        if not candidatas:
            return self._la_que_hace_mas_que_no_suena(oyente)
        # 3. Gana la de mayor puntaje. Si empatan, la de id más chico.
        return max(
            candidatas,
            key=lambda c: (sum(p(c, oyente) for p in self.puntajes), -c.id),
        )

    def _la_que_hace_mas_que_no_suena(self, oyente: Oyente) -> Cancion:
        ultima_vez = {}
        for posicion, escucha in enumerate(oyente.escuchas):
            ultima_vez[escucha.cancion.id] = posicion
        # Las que nunca sonaron tienen -1, así que van primero. Empate: id más chico.
        return min(
            self.catalogo.canciones,
            key=lambda c: (ultima_vez.get(c.id, -1), c.id),
        )

    def flujo(self, oyente: Oyente) -> Iterator[Emitible]:
        """Entrega de a un elemento, para siempre. Cada n_pausa canciones, una Pausa."""
        contador = 0
        while True:
            if contador == self.n_pausa:
                yield Pausa(self.duracion_pausa)
                contador = 0
            else:
                yield self.elegir_siguiente(oyente)
                contador += 1