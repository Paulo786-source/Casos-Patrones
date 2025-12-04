class Jugador:
    VIDA_INICIAL = 200

    def __init__(self, nombre):
        self.nombre = nombre
        self.vida_max = Jugador.VIDA_INICIAL
        self.vida = Jugador.VIDA_INICIAL
        self.artes_marciales = []  # lista de 3 artes

    # --- vida ---
    def recibir_damage(self, cantidad):
        if cantidad < 0:
            cantidad = 0
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    def curar(self, cantidad):
        if cantidad < 0:
            cantidad = 0
        self.vida += cantidad
        if self.vida > self.vida_max:
            self.vida = self.vida_max

    def esta_vivo(self):
        return self.vida > 0

    # --- artes ---
    def asignar_artes(self, artes):
        # se queda solo con los primeros 3 por seguridad
        self.artes_marciales = artes[:3]

    def elegir_arte(self, indice):
        return self.artes_marciales[indice]

    def resumen_vida(self):
        return str(self.vida) + " de " + str(self.vida_max)
