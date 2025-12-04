from concrete_arts import Taekwondo, Wushu, KungFu, Sambo, Sumo, Aikido, Judo, Boxing, Karate, Capoeira
class FabricaArtesMarciales:

    @staticmethod
    def crear_artes_disponibles():
        """
        Retorna una lista con las 10 artes marciales (Concrete Strategies).
        """
        return [
            Taekwondo(),
            Wushu(),
            Sumo(),
            KungFu(),
            Aikido(),
            Sambo(),
            Judo(),
            Boxing(),
            Karate(),
            Capoeira(),
        ]
