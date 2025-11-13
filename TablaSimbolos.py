import tkinter as tk
from tkinter import ttk, messagebox

class TablaSimbolos:
    def __init__(self, root, analizador_lexico):
        self.root = root
        self.analizador_lexico = analizador_lexico


    def detectar_tipo_dato(self, token):
        """Clasifica valores (NUM, STR, ID, etc.)"""
        tipo = token["tipo"]
        valor = token["valor"]

        if tipo == "NUM":
            if "." in valor:
                return "decimal"
            return "entero"

        if tipo == "STR":
            return "cadena"

        if tipo == "ID":
            return "identificador"

        return "desconocido"


    def mostrar_tabla(self, tokens):
        if not tokens:
            messagebox.showwarning("No hay tokens para analizar")
            return

        tabla_simbolos = {}

        i = 0
        while i < len(tokens):

            tok = tokens[i]

            # --------------------------------------------
            # 1) ASIGNACIONES:    ID = valor
            # --------------------------------------------
            if tok["tipo"] == "ID" and i+1 < len(tokens) and tokens[i+1]["valor"] == "=":
                nombre = tok["valor"]

                if i+2 < len(tokens):
                    valor_token = tokens[i+2]
                    tipo_dato = self.detectar_tipo_dato(valor_token)
                    valor = valor_token["valor"]

                    tabla_simbolos[nombre] = {
                        "nombre": nombre,
                        "categoria": "variable",
                        "tipo": tipo_dato,
                        "valor": valor.strip('"')
                    }

                i += 3
                continue

            # --------------------------------------------
            # 2) CICLO FOR:    for i in ...
            # --------------------------------------------
            if tok["valor"] == "for" and i+1 < len(tokens) and tokens[i+1]["tipo"] == "ID":
                nombre = tokens[i+1]["valor"]  # variable del ciclo

                tabla_simbolos[nombre] = {
                    "nombre": nombre,
                    "categoria": "ciclo",
                    "tipo": "iterador",
                    "valor": "for"
                }

                i += 1
                continue

            # --------------------------------------------
            # 3) LLAMADAS A FUNCIÓN:   nombre(  )
            # --------------------------------------------
            if tok["tipo"] == "ID" and i+1 < len(tokens) and tokens[i+1]["valor"] == "(":

                nombre = tok["valor"]
                parametros = []

                j = i + 2
                while j < len(tokens) and tokens[j]["valor"] != ")":
                    if tokens[j]["tipo"] in ["ID", "NUM", "STR"]:
                        parametros.append(tokens[j]["valor"])
                    j += 1

                tabla_simbolos[nombre] = {
                    "nombre": nombre,
                    "categoria": "función",
                    "tipo": f"parámetros({len(parametros)})",
                    "valor": ", ".join(parametros)
                }

                i = j + 1
                continue

            i += 1

        # --------------------------------------------
        # Mostrar tabla en ventana
        # --------------------------------------------

        ventana = tk.Toplevel(self.root)
        ventana.title("Tabla de Símbolos")
        ventana.geometry("800x400")

        columnas = ("Símbolo", "Categoría", "Tipo", "Valor")
        tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=150, anchor="center")

        tabla.pack(fill=tk.BOTH, expand=True)

        for simb in tabla_simbolos.values():
            tabla.insert("", tk.END, values=(
                simb["nombre"], simb["categoria"], simb["tipo"], simb["valor"]
            ))
