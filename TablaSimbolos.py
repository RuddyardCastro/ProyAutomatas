import tkinter as tk
from tkinter import ttk, messagebox

class TablaSimbolos:
    def __init__(self, root, analizador_lexico):
        self.root = root
        self.analizador_lexico = analizador_lexico

    def mostrar_tabla(self, contenido):
        if not contenido.strip():
            messagebox.showwarning("Advertencia", "El área de texto está vacía.")
            return

        # Obtener tokens desde el analizador léxico
        tokens = self.analizador_lexico.separar_token(contenido)

    
        simbolos = []
        simbolos_unicos = set()

        for token in tokens:
            tipo = token["tipo"]
            valor = token["valor"]

            # Variables válidas
            if tipo == "ID" and valor not in simbolos_unicos:
                simbolos_unicos.add(valor)
                simbolos.append({
                    "nombre": valor,
                    "categoria": "Variable",
                    "tipo_dato": "Entero (int)",
                    "ambito": "Global"
                })

            # Palabras reservadas o funciones
            elif tipo == "PR" and valor not in simbolos_unicos:
                simbolos_unicos.add(valor)
                simbolos.append({
                    "nombre": valor,
                    "categoria": "Función" if valor.lower() == "print" else "Palabra Reservada",
                    "tipo_dato": "N/A (Predefinida)",
                    "ambito": "Global"
                })

        # Crear nueva ventana
        ventana_tabla = tk.Toplevel(self.root)
        ventana_tabla.title("Tabla de Símbolos")
        ventana_tabla.geometry("650x400")

        #Headder
        columnas = ("Nombre del Símbolo", "Categoría", "Tipo de Dato", "Ámbito")
        tabla = ttk.Treeview(ventana_tabla, columns=columnas, show='headings')
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor='center', width=150)
        tabla.pack(fill=tk.BOTH, expand=True)

        # Valores 
        for simb in simbolos:
            tabla.insert("", tk.END, values=(
                simb["nombre"], simb["categoria"], simb["tipo_dato"], simb["ambito"]
            ))

        
        scroll_y = ttk.Scrollbar(ventana_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscroll=scroll_y.set)
        scroll_y.pack(side="right", fill="y")

        
