from caso3.fabrica_artes import FabricaArtesMarciales
from jugador import Jugador
from motor_combate import MotorCombate
from bitacora import BitacoraCombate
import random

# ==================================================
# Función para elegir artes para un jugador
# ==================================================
def elegir_artes_para_jugador(jugador, artes_disponibles):
    print(f"\nSeleccione 3 artes marciales para {jugador.nombre}:\n")

    for i, a in enumerate(artes_disponibles):
        print(f"{i}. {a.nombre}")

    indices = []
    while len(indices) < 3:
        try:
            idx = int(input(f"\nElija arte #{len(indices)+1}: "))
            if 0 <= idx < len(artes_disponibles):
                indices.append(idx)
            else:
                print("Índice inválido.")
        except ValueError:
            print("Debe ingresar un número.")

    artes = [artes_disponibles[i] for i in indices]
    jugador.asignar_artes(artes)

    print(f"\n{jugador.nombre} eligió:")
    for a in jugador.artes_marciales:
        print(" -", a.nombre)


# ==================================================
# MAIN DEL JUEGO
# ==================================================
def main():
    print("=== JUEGO DE ARTES MARCIALES ===")

    # Crear jugadores
    j1 = Jugador("Jugador 1")
    j2 = Jugador("Jugador 2")

    # Obtener todas las estrategias
    artes_disponibles = FabricaArtesMarciales.crear_artes_disponibles()

    # Elegir artes para ambos jugadores
    elegir_artes_para_jugador(j1, artes_disponibles)
    elegir_artes_para_jugador(j2, artes_disponibles)

    # Mostrar artes resumidas
    print("\n--- Artes de Jugador 1 ---")
    for i, a in enumerate(j1.artes_marciales):
        print(f"{i}. {a.nombre} → {a.descripcion_golpes()}")

    print("\n--- Artes de Jugador 2 ---")
    for i, a in enumerate(j2.artes_marciales):
        print(f"{i}. {a.nombre} → {a.descripcion_golpes()}")

    # Preparar motor de combate
    bitacora = BitacoraCombate()
    motor = MotorCombate(j1, j2, bitacora)

    # Bucle de combate
    while not motor.juego_terminado():

        # ====================================
        # TURNO JUGADOR 1
        # ====================================
        print("\n=== Turno de Jugador 1 ===\n")
        for i, a in enumerate(j1.artes_marciales):
            print(f"{i}. {a.nombre}")

        idx = int(input("\nElija arte: "))
        r1 = motor.turno(j1, j2, idx)
        print("\n" + r1.resumen())

        if motor.juego_terminado():
            break

        # ====================================
        # TURNO JUGADOR 2
        # ====================================
        print("\n=== Turno de Jugador 2 ===\n")
        for i, a in enumerate(j2.artes_marciales):
            print(f"{i}. {a.nombre}")

        idx = int(input("\nElija arte: "))
        r2 = motor.turno(j2, j1, idx)
        print("\n" + r2.resumen())

        # Mostrar vidas
        print("\nVidas actuales:")
        print("Jugador 1:", j1.resumen_vida())
        print("Jugador 2:", j2.resumen_vida())

    # ==================================================
    # FIN DEL JUEGO
    # ==================================================
    print("\n=== JUEGO TERMINADO ===")
    ganador = motor.obtener_ganador()
    if ganador:
        print("¡Ganador:", ganador.nombre, "!")
    else:
        print("Hubo un empate.")

    print("\n--- BITÁCORA COMPLETA ---")
    bitacora.imprimir()


# ==================================================
# EJECUCIÓN
# ==================================================
if __name__ == "__main__":
    main()
