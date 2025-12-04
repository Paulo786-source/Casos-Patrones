import random
class ArteMarcial:
    """
    Strategy de ataque.
    Todas las artes marciales van a heredar de esta clase.

    - nombre: nombre del estilo (Karate, Box, etc.)
    - golpes: lista de 3 objetos Golpe
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self.golpes = []  # aquí se guardan 3 golpes

    def agregar_golpe(self, golpe):
        """Agregar un Golpe a la lista (normalmente se usa en el __init__ de las hijas)."""
        self.golpes.append(golpe)

    def generar_combo(self):
        """
        Devuelve una lista de 3 a 6 golpes elegidos aleatoriamente
        de los 3 golpes que tiene este estilo.
        Esta es la 'estrategia' por defecto.
        """
        cantidad = random.randint(3, 6)
        combo = []
        for _ in range(cantidad):
            golpe = random.choice(self.golpes)
            combo.append(golpe)
        return combo

    def descripcion_golpes(self):
        """
        Devuelve un string para la UI, por ejemplo:
        'Mae Geri 10 | Mae Geri fuerte 15 | Yoko Geri 8'
        """
        partes = []
        for g in self.golpes:
            partes.append(g.nombre + " " + str(g.damage_base))
        return " | ".join(partes)
