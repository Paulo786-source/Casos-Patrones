class BitacoraCombate:
    def __init__(self):
        self.lineas = []

    def agregar_linea(self, texto):
        self.lineas.append(texto)

    def agregar_bloque(self, lista_textos):
        for t in lista_textos:
            self.agregar_linea(t)

    def imprimir(self):
        print("===== BITÁCORA =====")
        for linea in self.lineas:
            print(linea)
        print("====================")
