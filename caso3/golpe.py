import random

class Golpe:
    def __init__(self, nombre, damage_base, cura_usuario=0, damage_extra_enemigo=0):
        self.nombre = nombre
        self.damage_base = damage_base
        self.cura_usuario = cura_usuario
        self.damage_extra_enemigo = damage_extra_enemigo

    def aplicar(self, atacante, defensor):
        """Aplica el golpe: resta vida al enemigo y puede curar al usuario."""
        damage_total = self.damage_base + self.damage_extra_enemigo
        defensor.recibir_damage(damage_total)

        if self.cura_usuario > 0:
            atacante.curar(self.cura_usuario)

    def resumen(self):
        """Texto corto para bitácora."""
        partes = [self.nombre]
        if self.cura_usuario > 0:
            partes.append("(cura +" + str(self.cura_usuario) + ")")
        if self.damage_extra_enemigo > 0:
            partes.append("(extra +" + str(self.damage_extra_enemigo) + " daño)")
        return " ".join(partes)
