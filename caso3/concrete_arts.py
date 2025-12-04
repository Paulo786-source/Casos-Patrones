# ===== 10 Concrete Strategies =====
from artemarcial import ArteMarcial
from golpe import Golpe

class Taekwondo(ArteMarcial):
    def __init__(self):
        super().__init__("Taekwondo")
        self.golpes = [
            Golpe("Ap Chagi", 12),
            Golpe("Dollyo Chagi", 18),
            Golpe("Yop Chagi", 15),
        ]


class Wushu(ArteMarcial):
    def __init__(self):
        super().__init__("Wushu")
        self.golpes = [
            Golpe("Puño recto", 10),
            Golpe("Patada giratoria", 20),
            Golpe("Golpe de palma", 14, cura_usuario=5),
        ]


class Sumo(ArteMarcial):
    def __init__(self):
        super().__init__("Sumo")
        self.golpes = [
            Golpe("Empujón", 16),
            Golpe("Golpe de hombro", 18),
            Golpe("Carga completa", 22, damage_extra_enemigo=5),
        ]



class KungFu(ArteMarcial):
    def __init__(self):
        super().__init__("Kung Fu")
        self.golpes = [
            Golpe("Ch'en", 11),
            Golpe("Kun tsu", 10),
            # Pei tsu: +10 vida al usuario y +5 daño extra al enemigo
            Golpe("Pei tsu", 8, cura_usuario=10, damage_extra_enemigo=5),
        ]


class Aikido(ArteMarcial):
    def __init__(self):
        super().__init__("Aikido")
        self.golpes = [
            Golpe("Proyección básica", 12),
            Golpe("Luxación", 15),
            Golpe("Contraataque fluido", 10, cura_usuario=8),
        ]


class Sambo(ArteMarcial):
    def __init__(self):
        super().__init__("Sambo")
        self.golpes = [
            Golpe("Derribo doble pierna", 17),
            Golpe("Proyección de cadera", 19),
            Golpe("Llave de brazo", 14, damage_extra_enemigo=6),
        ]


class Judo(ArteMarcial):
    def __init__(self):
        super().__init__("Judo")
        self.golpes = [
            Golpe("O Soto Gari", 16),
            Golpe("Seoi Nage", 18),
            Golpe("Koshi Guruma", 20),
        ]


class Boxing(ArteMarcial):
    def __init__(self):
        super().__init__("Boxing")
        self.golpes = [
            Golpe("Jab", 5),
            Golpe("Gancho", 12),
            Golpe("Uppercut", 18),
        ]


class Karate(ArteMarcial):
    def __init__(self):
        super().__init__("Karate")
        self.golpes = [
            Golpe("Mae Geri", 10),
            Golpe("Mae Geri fuerte", 15),
            # Yoko Geri: +10 de vida al usuario
            Golpe("Yoko Geri", 8, cura_usuario=10),
        ]


class Capoeira(ArteMarcial):
    def __init__(self):
        super().__init__("Capoeira")
        self.golpes = [
            Golpe("Meia-lua de frente", 14),
            Golpe("Armada", 18),
            Golpe("Mortal giratorio", 20, damage_extra_enemigo=5),
        ]
