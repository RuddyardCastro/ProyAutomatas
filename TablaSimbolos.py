import tkinter as tk
from tkinter import ttk, messagebox
# Nota: La importación de Separador_Lexico debe estar en GUI.py y no es necesaria aquí si se pasa por constructor.

class TablaSimbolos:
    def __init__(self, root, analizador_lexico):
        self.root = root
        # El analizador léxico se pasa para obtener los tokens una sola vez.
        self.analizador_lexico = analizador_lexico
    
    def _obtener_tipo_y_categoria(self, tipo, valor):
        """
        Realiza el análisis semántico usando el resultado léxico.
        Utiliza 'tipo' y 'valor' para asignar la Categoría y Tipo de Dato.
        """
        
        # --- Lógica de Palabras Reservadas (PR) ---
        if tipo == "PR":
            valor_up = valor.upper()
            
            # [cite_start]1. Clasificación Booleana (si están en PR.txt [cite: 3])
            if valor_up == "TRUE" or valor_up == "FALSE":
                return "Constante", "Booleano (bool)"
            
            # 2. PRs de control de flujo
            elif valor_up in ["DEF", "IMPORT", "FOR", "WHILE", "IF", "ELSE", "ELIF", "RETURN"]:
                return "Palabra Reservada", "(Control)"
            
            # 3. Funciones predefinidas
            elif valor_up == "PRINT":
                return "Función", "(Predefinida)"
            
            # [cite_start]4. PRs mal clasificadas que deberían ser ID (self, tkinter, as, etc.) [cite: 3]
            elif valor_up in ["SELF", "TKINTER", "AS", "TOKEN", "SPLITLINES"]:
                if valor_up == "SELF":
                    # Si bien está mal clasificado, semánticamente es un parámetro
                    return "Parámetro/Instancia", "Objeto de Instancia"
                return "Identificador/Componente", "Error Léxico/ID"
        
        # --- Lógica de Números (NUM) ---
        elif tipo == "NUM":
            # Se usa el valor para distinguir entre Entero (int) y Decimal (float)
            if "." in valor:
                return "Literal Numérico", "Decimal (float)"
            else:
                return "Literal Numérico", "Entero (int)"

        # --- Lógica de Cadenas (STR) ---
        elif tipo == "STR":
            return "Literal", "Cadena (str)"
            
        # --- Lógica de Identificadores (ID) ---
        elif tipo == "ID":
            valor_low = valor.lower()
            
            # Manejo de identificadores especiales (si se hubieran clasificado correctamente como ID)
            if valor_low == "self":
                return "Parámetro/Instancia", "Objeto de Instancia"
            elif valor_low == "tk":
                return "Módulo/Biblioteca", "Objeto Módulo"
            
            # Constantes (ej. tk.LEFT)
            elif valor.isupper():
                return "Constante de Clase", "Constante"

            # Variables/Funciones/Métodos
            else:
                # Categorización basada en el contexto del código
                if valor in ["crear_menu1", "abrir_archivo", "guardar", "cerrar"]:
                    return "Función/Método", "Referencia de Función"
                elif valor in ["menubar", "menu_archivo"]:
                    return "Variable Local", "Objeto tk.Menu"
                return "Variable/ID", "Objeto (vario)"
        
        return "Desconocido", "Error de Tipo"


    def mostrar_tabla(self, contenido):
        if not contenido.strip():
            messagebox.showwarning("Advertencia", "El área de texto está vacía.")
            return

        # PASO 1: Obtener tokens (Clasificación Léxica única)
        tokens = self.analizador_lexico.separar_token(contenido)

        simbolos = []
        simbolos_unicos = set()

        for token in tokens:
            tipo = token["tipo"]
            valor = token["valor"]
            
            # Solo procesamos elementos que se muestran en la tabla
            if tipo in ["ID", "PR", "NUM", "STR"]:
                
                # Clave para unicidad (para evitar repetición de "Abrir", "Guardar", etc.)
                nombre_clave = valor if tipo in ["ID", "PR"] else f"{tipo}_{valor}"
                
                if nombre_clave not in simbolos_unicos:
                    simbolos_unicos.add(nombre_clave)
                    
                    # PASO 2: Obtener Categoría y Tipo de Dato (Análisis Semántico)
                    categoria, tipo_dato = self._obtener_tipo_y_categoria(tipo, valor)
                    
                    simbolos.append({
                        "nombre": valor,
                        "categoria": categoria,
                        "tipo_dato": tipo_dato,
                    })

        # --- Creación de la Interfaz (SOLO 3 Columnas) ---
        ventana_tabla = tk.Toplevel(self.root)
        ventana_tabla.title("Tabla de Símbolos")
        ventana_tabla.geometry("750x400")

        # Headder con 3 columnas
        columnas = ("Nombre del Símbolo", "Categoría", "Tipo de Dato")
        tabla = ttk.Treeview(ventana_tabla, columns=columnas, show='headings')
        
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor='center', width=250)
        
        tabla.pack(fill=tk.BOTH, expand=True)

        # Valores
        for simb in simbolos:
            tabla.insert("", tk.END, values=(
                simb["nombre"], simb["categoria"], simb["tipo_dato"]
            ))

        # Scrollbar
        scroll_y = ttk.Scrollbar(ventana_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscroll=scroll_y.set)
        scroll_y.pack(side="right", fill="y")