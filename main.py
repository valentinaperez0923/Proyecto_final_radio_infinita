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


def texto_cancion(numero: int, cancion: Cancion, completa: bool) -> str:
    """Función pura: arma el texto de una canción (no imprime nada)."""
    como = "completa" if completa else "cortada"
    return (f"{numero:2}. {cancion.titulo} - {cancion.artista} "
            f"(energía {cancion.energia}) -> {como}")


def texto_pausa(numero: int, duracion: float) -> str:
    """Función pura: arma el texto de una pausa."""
    return f"{numero:2}. --- Pausa de {duracion:.0f} segundos ---"


def main(cantidad: int = 12) -> None:
    radio = Radio(
        CATALOGO,
        puntajes=[afinidad, energia_objetivo(8)],
        filtros=[variedad(2), no_repetir_cancion(10)],
        n_pausa=4,
        duracion_pausa=60,
    )
    oyente = Oyente("Ana")

    # islice corta el flujo infinito después de `cantidad` elementos.
    flujo = islice(radio.flujo(oyente), cantidad)

    for numero, elemento in enumerate(flujo, 1):
        if isinstance(elemento, Cancion):
            completa = escucho_completa(elemento)
            oyente.registrar_escucha(elemento, completa)  # la radio aprende
            print(texto_cancion(numero, elemento, completa))
        else:
            print(texto_pausa(numero, elemento.duracion))


if __name__ == "__main__":
    main()