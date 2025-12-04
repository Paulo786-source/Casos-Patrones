import tkinter as tk
from tkinter import messagebox

from fabrica_artes import FabricaArtesMarciales
from jugador import Jugador


class JuegoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Artes Marciales")

        # === CONFIGURACIÓN DE GRID PARA AUTOAJUSTE ===
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)  # centro crece más
        self.root.columnconfigure(2, weight=1)

        self.root.rowconfigure(0, weight=1)

        # Crear jugadores
        self.j1 = Jugador("Player 1")
        self.j2 = Jugador("Player 2")

        # Artes disponibles
        self.artes_disponibles = FabricaArtesMarciales.crear_artes_disponibles()

        # Selección inicial de artes
        self.seleccionar_artes_para_jugador(self.j1, "Seleccionar artes para Player 1")
        self.seleccionar_artes_para_jugador(self.j2, "Seleccionar artes para Player 2")

        # Estado de turnos
        self.j1_arte_sel = 0
        self.j2_arte_sel = 0
        self.j1_combo_pendiente = None
        self.j2_combo_pendiente = None

        self.estado_j1 = "esperando_seleccion"
        self.estado_j2 = "esperando_seleccion"

        self.turno_actual = 1

        # Contadores
        self.j1_contador_combos = 0
        self.j2_contador_combos = 0

        # UI
        self.crear_ui()
        self.refrescar_artes_ui()
        self.actualizar_vidas()
        self.actualizar_controles()

    # ============================================================
    # SELECCIÓN DE ARTES
    # ============================================================
    def seleccionar_artes_para_jugador(self, jugador, titulo):
        win = tk.Toplevel(self.root)
        win.title(titulo)

        tk.Label(win, text=f"Seleccione 3 artes para {jugador.nombre}:").pack(pady=5)

        listbox = tk.Listbox(win, selectmode=tk.MULTIPLE, width=40)
        for i, arte in enumerate(self.artes_disponibles):
            listbox.insert(tk.END, f"{i}. {arte.nombre}")
        listbox.pack(padx=10, pady=5)

        def confirmar():
            seleccion = listbox.curselection()
            if len(seleccion) != 3:
                messagebox.showerror("Error", "Debe seleccionar exactamente 3 artes.")
                return
            jugador.asignar_artes([self.artes_disponibles[i] for i in seleccion])
            win.destroy()

        tk.Button(win, text="Confirmar", command=confirmar).pack(pady=5)

        win.grab_set()
        self.root.wait_window(win)

    # ============================================================
    # LOGICA COMBATE
    # ============================================================
    def aplicar_combo(self, atacante, defensor, combo):
        damage_total = 0
        cura_total = 0
        nombres = []
        especial = None

        for golpe in combo:
            nombres.append(golpe.nombre)
            vida_def_antes = defensor.vida
            vida_atk_antes = atacante.vida

            golpe.aplicar(atacante, defensor)

            damage = max(0, vida_def_antes - defensor.vida)
            cura = max(0, atacante.vida - vida_atk_antes)

            damage_total += damage
            cura_total += cura

            if golpe.cura_usuario > 0 or golpe.damage_extra_enemigo > 0:
                especial = golpe

        return damage_total, cura_total, nombres, especial

    # ============================================================
    # UI
    # ============================================================
    def crear_ui(self):
        # === FRAMES PRINCIPALES ===
        self.frame_p1 = tk.Frame(self.root, padx=10, pady=10, bd=2, relief="groove")
        self.frame_centro = tk.Frame(self.root, padx=10, pady=10)
        self.frame_p2 = tk.Frame(self.root, padx=10, pady=10, bd=2, relief="groove")

        self.frame_p1.grid(row=0, column=0, sticky="nsew")
        self.frame_centro.grid(row=0, column=1, sticky="nsew")
        self.frame_p2.grid(row=0, column=2, sticky="nsew")

        # ---------------- PLAYER 1 ----------------
        tk.Label(self.frame_p1, text="Player 1", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3)

        self.j1_btn_artes = []
        self.j1_lbl_golpes = []

        for i in range(3):
            btn = tk.Button(self.frame_p1, text="", width=12,
                            command=lambda idx=i: self.seleccionar_arte_p1(idx),
                            bg="#b33", fg="white")
            btn.grid(row=1, column=i, padx=5, pady=5)
            self.j1_btn_artes.append(btn)

        for i in range(3):
            lbl = tk.Label(self.frame_p1, text="", font=("Arial", 8))
            lbl.grid(row=2, column=i)
            self.j1_lbl_golpes.append(lbl)

        self.btn_sel_arte_p1 = tk.Button(self.frame_p1, text="Seleccionar arte marcial",
                                         command=self.fijar_arte_p1, bg="#d2b48c")
        self.btn_sel_arte_p1.grid(row=3, column=0, columnspan=3, pady=5)

        self.btn_combo_p1 = tk.Button(self.frame_p1, text="Generar combo",
                                      command=self.generar_combo_p1, bg="#f0a500")
        self.btn_combo_p1.grid(row=4, column=0, columnspan=3, pady=5)

        self.btn_atacar_p1 = tk.Button(self.frame_p1, text="Atacar",
                                       command=self.atacar_p1, bg="#e25822", fg="white")
        self.btn_atacar_p1.grid(row=5, column=0, columnspan=3, pady=5)

        self.txt_log_p1 = tk.Text(self.frame_p1, height=4, width=38)
        self.txt_log_p1.grid(row=6, column=0, columnspan=3)

        # ---------------- PLAYER 2 ----------------
        tk.Label(self.frame_p2, text="Player 2", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3)

        self.j2_btn_artes = []
        self.j2_lbl_golpes = []

        for i in range(3):
            btn = tk.Button(self.frame_p2, text="", width=12,
                            command=lambda idx=i: self.seleccionar_arte_p2(idx),
                            bg="#b33", fg="white")
            btn.grid(row=1, column=i, padx=5, pady=5)
            self.j2_btn_artes.append(btn)

        for i in range(3):
            lbl = tk.Label(self.frame_p2, text="", font=("Arial", 8))
            lbl.grid(row=2, column=i)
            self.j2_lbl_golpes.append(lbl)

        self.btn_sel_arte_p2 = tk.Button(self.frame_p2, text="Seleccionar arte marcial (P2)",
                                         command=self.fijar_arte_p2, bg="#d2b48c")
        self.btn_sel_arte_p2.grid(row=3, column=0, columnspan=3, pady=5)

        self.btn_combo_p2 = tk.Button(self.frame_p2, text="Generar combo",
                                      command=self.generar_combo_p2, bg="#f0a500")
        self.btn_combo_p2.grid(row=4, column=0, columnspan=3, pady=5)

        self.btn_atacar_p2 = tk.Button(self.frame_p2, text="Atacar",
                                       command=self.atacar_p2, bg="#e25822", fg="white")
        self.btn_atacar_p2.grid(row=5, column=0, columnspan=3, pady=5)

        self.txt_log_p2 = tk.Text(self.frame_p2, height=4, width=38)
        self.txt_log_p2.grid(row=6, column=0, columnspan=3)

        # ---------------- CENTRO ----------------
        tk.Label(self.frame_centro, text="VIDAS", font=("Arial", 13, "bold")).grid(row=0, column=0, pady=5)

        self.lbl_vida_j1 = tk.Label(self.frame_centro, text="")
        self.lbl_vida_j1.grid(row=1, column=0, pady=5)

        self.lbl_vida_j2 = tk.Label(self.frame_centro, text="")
        self.lbl_vida_j2.grid(row=2, column=0, pady=5)

        tk.Label(self.frame_centro, text="Bitácora:", font=("Arial", 12)).grid(row=3, column=0, pady=10)

        # Bitácora compacta
        self.txt_bitacora = tk.Text(self.frame_centro, height=12, width=45)
        self.txt_bitacora.grid(row=4, column=0)

        self.lbl_especial = tk.Label(self.frame_centro, text="Última habilidad: (ninguna)")
        self.lbl_especial.grid(row=5, column=0, pady=10)

    # ============================================================
    # REFRESCAR UI
    # ============================================================
    def refrescar_artes_ui(self):
        for i, arte in enumerate(self.j1.artes_marciales):
            self.j1_btn_artes[i].config(text=arte.nombre)
            self.j1_lbl_golpes[i].config(text=arte.descripcion_golpes())

        for i, arte in enumerate(self.j2.artes_marciales):
            self.j2_btn_artes[i].config(text=arte.nombre)
            self.j2_lbl_golpes[i].config(text=arte.descripcion_golpes())

    def actualizar_vidas(self):
        self.lbl_vida_j1.config(text=self.j1.resumen_vida())
        self.lbl_vida_j2.config(text=self.j2.resumen_vida())

    # ============================================================
    # SELECCIÓN DE ARTE
    # ============================================================
    def seleccionar_arte_p1(self, idx):
        self.j1_arte_sel = idx
        for i, b in enumerate(self.j1_btn_artes):
            b.config(relief="sunken" if i == idx else "raised")

    def seleccionar_arte_p2(self, idx):
        self.j2_arte_sel = idx
        for i, b in enumerate(self.j2_btn_artes):
            b.config(relief="sunken" if i == idx else "raised")

    # ============================================================
    # FIJAR ARTE
    # ============================================================
    def fijar_arte_p1(self):
        if self.turno_actual != 1:
            return
        if self.estado_j1 != "esperando_seleccion":
            return

        self.estado_j1 = "arte_fijado"
        self.actualizar_controles()

    def fijar_arte_p2(self):
        if self.turno_actual != 2:
            return
        if self.estado_j2 != "esperando_seleccion":
            return

        self.estado_j2 = "arte_fijado"
        self.actualizar_controles()

    # ============================================================
    # GENERAR COMBOS
    # ============================================================
    def generar_combo_p1(self):
        if self.turno_actual != 1:
            return
        if self.estado_j1 != "arte_fijado":
            messagebox.showinfo("Error", "Debe fijar el arte antes de generar el combo.")
            return

        arte = self.j1.artes_marciales[self.j1_arte_sel]
        self.j1_combo_pendiente = arte.generar_combo()
        self.estado_j1 = "combo_generado"

        nombres = ", ".join(g.nombre for g in self.j1_combo_pendiente)
        self.txt_bitacora.insert(tk.END, f"P1 genera combo: {nombres}\n")
        self.txt_bitacora.see(tk.END)

        self.actualizar_controles()

    def generar_combo_p2(self):
        if self.turno_actual != 2:
            return
        if self.estado_j2 != "arte_fijado":
            messagebox.showinfo("Error", "Debe fijar el arte antes de generar el combo.")
            return

        arte = self.j2.artes_marciales[self.j2_arte_sel]
        self.j2_combo_pendiente = arte.generar_combo()
        self.estado_j2 = "combo_generado"

        nombres = ", ".join(g.nombre for g in self.j2_combo_pendiente)
        self.txt_bitacora.insert(tk.END, f"P2 genera combo: {nombres}\n")
        self.txt_bitacora.see(tk.END)

        self.actualizar_controles()

    # ============================================================
    # ATAQUES
    # ============================================================
    def atacar_p1(self):
        if self.turno_actual != 1:
            return
        if self.estado_j1 != "combo_generado":
            messagebox.showinfo("Error", "Debe generar un combo antes de atacar.")
            return

        arte = self.j1.artes_marciales[self.j1_arte_sel]
        dmg, c, nombres, esp = self.aplicar_combo(self.j1, self.j2, self.j1_combo_pendiente)

        self.j1_contador_combos += 1
        linea = f"P1 ataca con {arte.nombre} ({', '.join(nombres)}) → daño {dmg}, cura {c}\n"

        self.txt_log_p1.insert(tk.END, linea)
        self.txt_bitacora.insert(tk.END, linea)
        self.txt_bitacora.see(tk.END)

        if esp:
            self.lbl_especial.config(text=f"Última habilidad: {esp.nombre} (+{esp.cura_usuario} vida, +{esp.damage_extra_enemigo} daño extra)")

        self.j1_combo_pendiente = None
        self.estado_j1 = "esperando_seleccion"
        self.turno_actual = 2

        self.actualizar_vidas()
        self.verificar_fin()
        self.actualizar_controles()

    def atacar_p2(self):
        if self.turno_actual != 2:
            return
        if self.estado_j2 != "combo_generado":
            messagebox.showinfo("Error", "Debe generar un combo antes de atacar.")
            return

        arte = self.j2.artes_marciales[self.j2_arte_sel]
        dmg, c, nombres, esp = self.aplicar_combo(self.j2, self.j1, self.j2_combo_pendiente)

        self.j2_contador_combos += 1
        linea = f"P2 ataca con {arte.nombre} ({', '.join(nombres)}) → daño {dmg}, cura {c}\n"

        self.txt_log_p2.insert(tk.END, linea)
        self.txt_bitacora.insert(tk.END, linea)
        self.txt_bitacora.see(tk.END)

        if esp:
            self.lbl_especial.config(text=f"Última habilidad: {esp.nombre} (+{esp.cura_usuario} vida, +{esp.damage_extra_enemigo} daño extra)")

        self.j2_combo_pendiente = None
        self.estado_j2 = "esperando_seleccion"
        self.turno_actual = 1

        self.actualizar_vidas()
        self.verificar_fin()
        self.actualizar_controles()

    # ============================================================
    # CONTROL DE BOTONES
    # ============================================================
    def actualizar_controles(self):
        # ---------- PLAYER 1 ----------
        if self.turno_actual == 1:
            for b in self.j1_btn_artes:
                b.config(state="normal" if self.estado_j1 == "esperando_seleccion" else "disabled")

            self.btn_sel_arte_p1.config(state="normal" if self.estado_j1 == "esperando_seleccion" else "disabled")
            self.btn_combo_p1.config(state="normal" if self.estado_j1 == "arte_fijado" else "disabled")
            self.btn_atacar_p1.config(state="normal" if self.estado_j1 == "combo_generado" else "disabled")

            # P2 deshabilitado
            for b in self.j2_btn_artes:
                b.config(state="disabled")
            self.btn_sel_arte_p2.config(state="disabled")
            self.btn_combo_p2.config(state="disabled")
            self.btn_atacar_p2.config(state="disabled")

        # ---------- PLAYER 2 ----------
        else:
            for b in self.j2_btn_artes:
                b.config(state="normal" if self.estado_j2 == "esperando_seleccion" else "disabled")

            self.btn_sel_arte_p2.config(state="normal" if self.estado_j2 == "esperando_seleccion" else "disabled")
            self.btn_combo_p2.config(state="normal" if self.estado_j2 == "arte_fijado" else "disabled")
            self.btn_atacar_p2.config(state="normal" if self.estado_j2 == "combo_generado" else "disabled")

            # P1 deshabilitado
            for b in self.j1_btn_artes:
                b.config(state="disabled")
            self.btn_sel_arte_p1.config(state="disabled")
            self.btn_combo_p1.config(state="disabled")
            self.btn_atacar_p1.config(state="disabled")

    # ============================================================
    # FIN DEL JUEGO
    # ============================================================
    def verificar_fin(self):
        if not self.j1.esta_vivo() or not self.j2.esta_vivo():
            ganador = (
                self.j1.nombre if self.j1.esta_vivo() else
                self.j2.nombre if self.j2.esta_vivo() else
                "Empate"
            )
            messagebox.showinfo("Fin del juego", f"Ganador: {ganador}")
            self.btn_atacar_p1.config(state="disabled")
            self.btn_atacar_p2.config(state="disabled")
            self.btn_combo_p1.config(state="disabled")
            self.btn_combo_p2.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoGUI(root)
    root.mainloop()
