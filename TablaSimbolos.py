import tkinter as tk
from tkinter import ttk, messagebox

class TablaSimbolos:
    def __init__(self, root):
        self.root = root   


    #--Se usa abajo
    def detectar_tipo_dato(self, token):
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


    #Val tab sinbolos
    def mostrar_tabla(self, tokens):
        if not tokens:
            messagebox.showwarning("No hay tokens para analizar")
            return

        tabla_simbolos = {}

        i = 0
        while i < len(tokens):

            tok = tokens[i]

           #val para ide
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

            #ciclos
            if tok["valor"] == "for" and i+1 < len(tokens) and tokens[i+1]["tipo"] == "ID":

                nombre = tokens[i+1]["valor"]

                tabla_simbolos[nombre] = {
                    "nombre": nombre,
                    "categoria": "ciclo",
                    "tipo": "iterador",
                    "valor": "for"
                }
            if tok["valor"] == "while" and i+1 < len(tokens) and tokens[i+1]["tipo"] == "ID":

                nombre = tokens[i+1]["valor"]

                tabla_simbolos[nombre] = {
                    "nombre": nombre,
                    "categoria": "ciclo",
                    "tipo": "iterador",
                    "valor": "while"
                }

                i += 1
                continue

           #Funcones parametros
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



            if tok["tipo"] == "ID" and tok["valor"] not in tabla_simbolos:
                 tabla_simbolos[tok["valor"]] = {
                    "nombre": tok["valor"],
                    "categoria": "variable",
                    "tipo": "identificador",
                    "valor": "-"
                }

            i += 1

       

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
