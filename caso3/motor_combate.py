from resultado_ataque import ResultadoAtaque
import random
class MotorCombate:
    def __init__(self, jugador1, jugador2, bitacora):
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.bitacora = bitacora

    def turno(self, atacante, defensor, indice_arte):
        arte = atacante.elegir_arte(indice_arte)
        combo = arte.generar_combo()

        damage_total = 0
        cura_total = 0
        lista_golpes = []

        for golpe in combo:
            lista_golpes.append(golpe.nombre)

            vida_def_antes = defensor.vida
            vida_atk_antes = atacante.vida

            golpe.aplicar(atacante, defensor)

            damage = max(0, vida_def_antes - defensor.vida)
            cura = max(0, atacante.vida - vida_atk_antes)

            damage_total += damage
            cura_total += cura

        resultado = ResultadoAtaque(
            atacante, defensor, arte, combo,
            damage_total, cura_total, lista_golpes
        )

        self.bitacora.agregar_bloque(resultado.resumen().split("\n"))
        return resultado

    def juego_terminado(self):
        return not self.jugador1.esta_vivo() or not self.jugador2.esta_vivo()

    def obtener_ganador(self):
        if self.jugador1.esta_vivo() and not self.jugador2.esta_vivo():
            return self.jugador1
        if self.jugador2.esta_vivo() and not self.jugador1.esta_vivo():
            return self.jugador2
        return None
