import tkinter as tk
from tkinter import ttk, messagebox

# Importamos tu lógica del programa
from sandwiches import (
    PolloSandwich, PavoSandwich, BeefSandwich, AtunSandwich,
    JamonSandwich, VegetarianoSandwich,
    Aguacate, DobleProteina, Queso, Sopa,
    LechugaExtra, TomateExtra,
    Orden
)

# -------------------------------------------------------
# PRECIOS PARA MOSTRAR EN LA GUI (NO afectan la lógica)
# -------------------------------------------------------

SANDWICH_PRICES = {
    "Pollo":  {15: 12.0, 30: 16.0},
    "Pavo":   {15: 12.0, 30: 16.0},
    "Beef":   {15: 14.0, 30: 18.0},
    "Atún":   {15: 13.0, 30: 17.0},
    "Jamón":  {15: 11.0, 30: 15.0},
    "Vegetariano": {15: 10.0, 30: 14.0},
}

ADICIONAL_PRICES = {
    "Aguacate":       {15: 1.5, 30: 2.0},
    "Doble proteína": {15: 4.5, 30: 6.0},
    "Queso":          {15: 1.0, 30: 1.5},
    "Sopa":           {15: 4.2, 30: 4.2},  # Mismo precio
    "Lechuga extra":  {15: 0.5, 30: 0.8},
    "Tomate extra":   {15: 0.5, 30: 0.8},
}

# Mapeos a las clases reales
SANDWICH_TYPES = {
    "Pollo": PolloSandwich,
    "Pavo": PavoSandwich,
    "Beef": BeefSandwich,
    "Atún": AtunSandwich,
    "Jamón": JamonSandwich,
    "Vegetariano": VegetarianoSandwich,
}

ADICIONALES = {
    "Aguacate": Aguacate,
    "Doble proteína": DobleProteina,
    "Queso": Queso,
    "Sopa": Sopa,
    "Lechuga extra": LechugaExtra,
    "Tomate extra": TomateExtra,
}

# -------------------------------------------------------
#              CLASE PRINCIPAL DE LA GUI
# -------------------------------------------------------

class SandwichGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurante - Sandwichería (Patrón Decorator)")
        self.root.geometry("820x650")

        # La orden completa
        self.orden = Orden()

        # ---------------------------
        # Selección de sándwich base
        # ---------------------------
        frame1 = tk.LabelFrame(root, text="Sándwich base", padx=10, pady=10)
        frame1.pack(fill="x", padx=10, pady=5)

        tk.Label(frame1, text="Tipo de sándwich:").grid(row=0, column=0, sticky="w")

        # Mostrar precios en el combobox
        self.combo_tipo = ttk.Combobox(
            frame1,
            values=[
                f"{nombre} (15cm: ₡{precios[15]} / 30cm: ₡{precios[30]})"
                for nombre, precios in SANDWICH_PRICES.items()
            ],
            state="readonly",
            width=40
        )
        self.combo_tipo.grid(row=0, column=1, padx=5)
        self.combo_tipo.current(0)

        tk.Label(frame1, text="Tamaño:").grid(row=1, column=0, sticky="w")
        self.size_var = tk.IntVar(value=15)
        tk.Radiobutton(frame1, text="15 cm", variable=self.size_var, value=15).grid(row=1, column=1, sticky="w")
        tk.Radiobutton(frame1, text="30 cm", variable=self.size_var, value=30).grid(row=1, column=2, sticky="w")

        # ---------------------------
        # Selección de adicionales
        # ---------------------------
        frame2 = tk.LabelFrame(root, text="Adicionales", padx=10, pady=10)
        frame2.pack(fill="x", padx=10, pady=5)

        self.adicional_vars = {}
        row = 0
        for nombre, precios in ADICIONAL_PRICES.items():
            texto = f"{nombre} (₡{precios[15]} / ₡{precios[30]})"
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame2, text=texto, variable=var)
            chk.grid(row=row, column=0, sticky="w")
            self.adicional_vars[nombre] = var
            row += 1

        # ---------------------------
        # Botón para agregar sándwich
        # ---------------------------
        btn_agregar = tk.Button(root, text="Agregar sándwich a la orden", command=self.agregar_sandwich)
        btn_agregar.pack(pady=10)

        # ---------------------------
        # Tabla profesional (Treeview)
        # ---------------------------
        frame3 = tk.LabelFrame(root, text="Detalle de la orden", padx=10, pady=10)
        frame3.pack(fill="both", expand=True, padx=10, pady=5)

        columnas = ("sandwich", "adicionales", "precio")

        self.tree = ttk.Treeview(frame3, columns=columnas, show="headings", height=12)
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("sandwich", text="Sándwich")
        self.tree.heading("adicionales", text="Adicionales")
        self.tree.heading("precio", text="Precio")

        self.tree.column("sandwich", width=230)
        self.tree.column("adicionales", width=470)
        self.tree.column("precio", width=100, anchor="e")

        scroll = ttk.Scrollbar(frame3, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        # ---------------------------
        # Label de total
        # ---------------------------
        self.label_total = tk.Label(root, text="TOTAL: ₡0.00", font=("Arial", 18, "bold"))
        self.label_total.pack(pady=10)

        # ---------------------------
        # Botón finalizar orden
        # ---------------------------
        btn_finalizar = tk.Button(root, text="Finalizar orden / Mostrar factura", command=self.refrescar_tabla)
        btn_finalizar.pack(pady=10)

    # -------------------------------------------------------
    # LÓGICA DE AGREGAR SÁNDWICH A LA ORDEN
    # -------------------------------------------------------
    def agregar_sandwich(self):
        texto_combo = self.combo_tipo.get()
        tipo = texto_combo.split(" (")[0]   # obtener el nombre real

        size = self.size_var.get()

        # Crear sándwich base
        sandwich = SANDWICH_TYPES[tipo](size)

        # Agregar adicionales según checkboxes
        for nombre, var in self.adicional_vars.items():
            if var.get():
                sandwich = ADICIONALES[nombre](sandwich)

        # Guardar en la orden
        self.orden.add_sandwich(sandwich)

        messagebox.showinfo("OK", "Sándwich agregado correctamente.")

        # Reset de checkboxes
        for var in self.adicional_vars.values():
            var.set(False)

        self.refrescar_tabla()

    # -------------------------------------------------------
    # REFRESCAR TABLA Y TOTAL
    # -------------------------------------------------------
    def refrescar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for s in self.orden.sandwiches:
            descripcion = s.get_description().split("($")[0]  # cortar precio base
            precio = f"{s.get_price():.2f}"

            partes = s.get_description().split("+")[1:]
            adicionales = ", ".join([p.strip() for p in partes]) if partes else "Ninguno"

            self.tree.insert("", "end", values=(descripcion, adicionales, precio))

        total = self.orden.calcular_total()
        self.label_total.config(text=f"TOTAL: ₡{total:.2f}")


# -------------------------------------------------------
#               EJECUCIÓN PRINCIPAL
# -------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    gui = SandwichGUI(root)
    root.mainloop()
