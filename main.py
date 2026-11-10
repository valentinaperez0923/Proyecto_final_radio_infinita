"""Programa principal: arma la radio, muestra el flujo y simula al oyente.

Acá viven los "efectos" (mostrar en pantalla y decidir cómo terminó cada
escucha). El resto del programa solo calcula.
"""

from itertools import islice

from modelo import Cancion, Oyente
from criterios import afinidad, energia_objetivo, variedad, no_repetir_cancion
from radio import Radio
from catalogo_datos import CATALOGO


def escucho_completa(cancion: Cancion) -> bool:
    """Oyente simulado: escucha enteras las canciones de energía 7 o más.

    Es una regla fija (no al azar), así que el programa da siempre lo mismo.
    """
    return cancion.energia >= 7


def main(cantidad: int = 12) -> None:
    radio = Radio(
        CATALOGO,
        puntajes=[afinidad, energia_objetivo(8)],
        filtros=[variedad(2), no_repetir_cancion(10)],
        n_pausa=4,
        duracion_pausa=60,
    )
    oyente = Oyente("Ana")

    for numero, elemento in enumerate(islice(radio.flujo(oyente), cantidad), 1):
        if isinstance(elemento, Cancion):
            completa = escucho_completa(elemento)
            oyente.registrar_escucha(elemento, completa)
            como = "completa" if completa else "cortada"
            print(f"{numero:2}. {elemento.titulo} - {elemento.artista} "
                  f"(energía {elemento.energia}) -> {como}")
        else:
            print(f"{numero:2}. --- Pausa de {elemento.duracion:.0f} segundos ---")


if __name__ == "__main__":
    main()