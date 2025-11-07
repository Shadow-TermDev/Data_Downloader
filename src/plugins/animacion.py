import time
import random
import sys
import threading

# C贸digos ANSI para manipular la terminal
OCULTAR_CURSOR = "\033[?25l"
MOSTRAR_CURSOR = "\033[?25h"
GUARDAR_POS = "\033[s"
RESTAURAR_POS = "\033[u"
LIMPIAR_LINEA = "\033[K"

# Caracteres de la animaci贸n
KATAKANA = list("銈€偒銈点偪銉娿儚銉炪儰銉┿儻")
BINARIOS = list("10")
CARACTERES = KATAKANA + BINARIOS

# 馃摫 **Tama帽o ajustado para parecer un mini celular**
ANCHO = 20  # M谩s angosto
ALTO = 15   # M谩s alto

def ejecutar_animacion(stop_event: threading.Event, color="\033[92m", velocidad=0.05):
    """
    Muestra una animaci贸n dentro de una ventanita.
    - Se muestra con una ca铆da fluida.
    - Se oculta con una desaparici贸n progresiva.
    """

    try:
        sys.stdout.write(OCULTAR_CURSOR)
        sys.stdout.write(GUARDAR_POS)
        sys.stdout.flush()

        pantalla = [[" " for _ in range(ANCHO)] for _ in range(ALTO)]
        posiciones = [random.randint(-ALTO, 0) for _ in range(ANCHO)]

        # **Aparici贸n fluida**
        for paso in range(ALTO):
            if stop_event.is_set():
                break
            sys.stdout.write(RESTAURAR_POS)
            for i in range(ALTO - paso):
                sys.stdout.write(" " * ANCHO + "\n")
            sys.stdout.flush()
            time.sleep(0.05)

        while not stop_event.is_set():
            sys.stdout.write(RESTAURAR_POS)

            for x in range(ANCHO):
                if random.random() > 0.9:  # Aumenta la frecuencia de actualizaci贸n
                    posiciones[x] = 0
                for y in range(ALTO):
                    if y == posiciones[x]:
                        pantalla[y][x] = random.choice(CARACTERES)
                    elif y < posiciones[x]:
                        pantalla[y][x] = " "

            # 鉁� **Evita desbordamientos en la 煤ltima l铆nea**
            for x in range(ANCHO):
                pantalla[ALTO - 1][x] = " "

            for linea in pantalla:
                sys.stdout.write(color + "".join(linea) + "\033[0m\n")

            sys.stdout.flush()
            time.sleep(velocidad)

            for i in range(len(posiciones)):
                if posiciones[i] < ALTO - 1:
                    posiciones[i] += 1

        # **Desaparici贸n fluida**
        for paso in range(ALTO, -1, -1):
            sys.stdout.write(RESTAURAR_POS)
            for i in range(ALTO):
                if i >= paso:
                    sys.stdout.write("\033[2K\n")
                else:
                    sys.stdout.write(color + "".join(pantalla[i]) + "\033[0m\n")
            sys.stdout.flush()
            time.sleep(0.05)

        # **Limpieza final**
        sys.stdout.write(RESTAURAR_POS)
        for _ in range(ALTO):
            sys.stdout.write("\033[2K\n")
        sys.stdout.write(RESTAURAR_POS)

    finally:
        sys.stdout.write(MOSTRAR_CURSOR)
        sys.stdout.flush()

