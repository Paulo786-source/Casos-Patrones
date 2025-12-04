class ResultadoAtaque:
    def __init__(self, atacante, defensor, arte_usada, combo,
                 damage_total, cura_total, lista_golpes):
        self.atacante = atacante
        self.defensor = defensor
        self.arte_usada = arte_usada
        self.combo = combo
        self.damage_total = damage_total
        self.cura_total = cura_total
        self.lista_golpes = lista_golpes

    def resumen(self):
        return (
            f"{self.atacante.nombre} realizó {len(self.combo)} golpes: "
            f"{', '.join(self.lista_golpes)}\n"
            f"Infringió un total de daño: {self.damage_total}\n"
            f"Recuperó un total de vida: {self.cura_total}\n"
        )
