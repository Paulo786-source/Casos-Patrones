from abc import ABC, abstractmethod
from typing import List

# ---------- Componente base ----------
class Sandwich(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def get_size(self) -> int:
        """Retorna 15 o 30"""
        pass

    def __str__(self):
        return f"{self.get_description()}  PRECIO {self.get_price():.2f}"


# ---------- Componentes concretos (sándwiches base) ----------
class BaseSandwich(Sandwich):
    def __init__(self, size: int):
        if size not in (15, 30):
            raise ValueError("Size must be 15 or 30")
        self._size = size

    def get_size(self) -> int:
        return self._size


class PolloSandwich(BaseSandwich):
    def __init__(self, size: int):
        super().__init__(size)
        self._price = 12.0 if size == 15 else 16.0

    def get_description(self) -> str:
        return f"Pollo de {self._size}cm (${self._price:.2f})"

    def get_price(self) -> float:
        return self._price


class PavoSandwich(BaseSandwich):
    def __init__(self, size: int):
        super().__init__(size)
        self._price = 12.0 if size == 15 else 16.0

    def get_description(self) -> str:
        return f"Pavo de {self._size}cm (${self._price:.2f})"

    def get_price(self) -> float:
        return self._price


class BeefSandwich(BaseSandwich):
    def __init__(self, size: int):
        super().__init__(size)
        self._price = 14.0 if size == 15 else 18.0

    def get_description(self) -> str:
        return f"Beef de {self._size}cm (${self._price:.2f})"

    def get_price(self) -> float:
        return self._price


class AtunSandwich(BaseSandwich):
    def __init__(self, size: int):
        super().__init__(size)
        self._price = 13.0 if size == 15 else 17.0

    def get_description(self) -> str:
        return f"Atún de {self._size}cm (${self._price:.2f})"

    def get_price(self) -> float:
        return self._price


class JamonSandwich(BaseSandwich):
    def __init__(self, size: int):
        super().__init__(size)
        self._price = 11.0 if size == 15 else 15.0

    def get_description(self) -> str:
        return f"Jamón de {self._size}cm (${self._price:.2f})"

    def get_price(self) -> float:
        return self._price


class VegetarianoSandwich(BaseSandwich):
    def __init__(self, size: int):
        super().__init__(size)
        self._price = 10.0 if size == 15 else 14.0

    def get_description(self) -> str:
        return f"Vegetariano de {self._size}cm (${self._price:.2f})"

    def get_price(self) -> float:
        return self._price


# ---------- Decorator base (adicionales) ----------
class AdicionalDecorator(Sandwich, ABC):
    def __init__(self, sandwich: Sandwich):
        self._sandwich = sandwich

    def get_size(self) -> int:
        return self._sandwich.get_size()


# ---------- Decoradores concretos ----------
class Aguacate(AdicionalDecorator):
    def get_description(self) -> str:
        adicional = self.get_price() - self._sandwich.get_price()
        return f"{self._sandwich.get_description()} + Aguacate (${adicional:.2f})"

    def get_price(self) -> float:
        return self._sandwich.get_price() + (1.5 if self.get_size() == 15 else 2.0)


class DobleProteina(AdicionalDecorator):
    def get_description(self) -> str:
        adicional = self.get_price() - self._sandwich.get_price()
        return f"{self._sandwich.get_description()} + Doble Proteína (${adicional:.2f})"

    def get_price(self) -> float:
        return self._sandwich.get_price() + (4.5 if self.get_size() == 15 else 6.0)


class Queso(AdicionalDecorator):
    def get_description(self) -> str:
        adicional = self.get_price() - self._sandwich.get_price()
        return f"{self._sandwich.get_description()} + Queso (${adicional:.2f})"

    def get_price(self) -> float:
        return self._sandwich.get_price() + (1.0 if self.get_size() == 15 else 1.5)


class Sopa(AdicionalDecorator):
    def get_description(self) -> str:
        adicional = self.get_price() - self._sandwich.get_price()
        return f"{self._sandwich.get_description()} + Sopa (${adicional:.2f})"

    def get_price(self) -> float:
        return self._sandwich.get_price() + 4.2


class LechugaExtra(AdicionalDecorator):
    def get_description(self) -> str:
        adicional = self.get_price() - self._sandwich.get_price()
        return f"{self._sandwich.get_description()} + Lechuga extra (${adicional:.2f})"

    def get_price(self) -> float:
        return self._sandwich.get_price() + (0.5 if self.get_size() == 15 else 0.8)


class TomateExtra(AdicionalDecorator):
    def get_description(self) -> str:
        adicional = self.get_price() - self._sandwich.get_price()
        return f"{self._sandwich.get_description()} + Tomate extra (${adicional:.2f})"

    def get_price(self) -> float:
        return self._sandwich.get_price() + (0.5 if self.get_size() == 15 else 0.8)


# ---------- Orden ----------
class Orden:
    def __init__(self):
        self.sandwiches: List[Sandwich] = []

    def add_sandwich(self, s: Sandwich):
        self.sandwiches.append(s)

    def calcular_total(self) -> float:
        return sum(s.get_price() for s in self.sandwiches)

    def detalle(self) -> str:
        lines = []
        lines.append("="*66)
        for s in self.sandwiches:
            lines.append(f"{s.get_description():70} PRECIO {s.get_price():.2f}")
        lines.append("="*66)
        lines.append(f"TOTAL {self.calcular_total():.2f}")
        return "\n".join(lines)


# ---------- Pruebas en terminal ----------
def pruebas_demo():
    orden = Orden()

    s1 = PavoSandwich(15)
    s1 = Aguacate(s1)
    s1 = DobleProteina(s1)
    orden.add_sandwich(s1)

    s2 = BeefSandwich(30)
    s2 = Sopa(s2)
    orden.add_sandwich(s2)

    s3 = PolloSandwich(15)
    orden.add_sandwich(s3)

    s4 = AtunSandwich(30)
    s4 = Queso(s4)
    s4 = Aguacate(s4)
    s4 = Aguacate(s4)
    orden.add_sandwich(s4)

    print(orden.detalle())


# Ejecutar pruebas si el archivo se ejecuta directo
if __name__ == "__main__":
    pruebas_demo()
