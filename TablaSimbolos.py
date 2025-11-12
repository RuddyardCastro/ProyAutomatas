import tkinter as tk
from tkinter import ttk, messagebox

class TablaSimbolos:
    def __init__(self, root, analizador_lexico):
        self.root = root
        self.analizador_lexico = analizador_lexico
    
    def _obtener_tipo_y_categoria(self, tipo, valor):
        
        if tipo == "PR":
            valor_up = valor.upper()
            
            if valor_up == "TRUE" or valor_up == "FALSE":
                return "Constante", "Booleano (bool)"
            
            elif valor_up in ["DEF", "IMPORT", "IF", "ELSE", "ELIF", "RETURN"]:
                return "Palabra Reservada", "(Control)"
            elif valor_up in ["FOR", "WHILE"]:
                return "Estructura de Control", "Ciclo"
            
            elif valor_up == "PRINT":
                return "Función", "(Predefinida)"
            
            elif valor_up in ["SELF", "TKINTER", "AS", "TOKEN", "SPLITLINES"]:
                if valor_up == "SELF":
                    return "Parámetro/Instancia", "Objeto de Instancia"
                return "Identificador/Componente", "Error Léxico/ID"
        
        elif tipo == "NUM":
            if "." in valor:
                return "Literal Numérico", "Decimal (float)"
            else:
                return "Literal Numérico", "Entero (int)"

        elif tipo == "STR":
            return "Literal", "Cadena (str)"
            
        elif tipo == "ID":
            valor_low = valor.lower()
            
            if valor_low == "self":
                return "Parámetro/Instancia", "Objeto de Instancia"
            elif valor_low == "tk":
                return "Módulo/Biblioteca", "Objeto Módulo"
            
            if valor.isupper():
                return "Constante de Clase", "Constante"
            
            if valor in ["crear_menu1", "abrir_archivo", "guardar", "cerrar", "limpiar_todo"]:
                return "Función/Método", "Referencia de Función"
            elif valor in ["menubar", "menu_archivo", "marco_principal", "ventana1", "scroll_text1", "analizador_lexico", "analizador_sintactico"]:
                return "Variable/Objeto", "Objeto (vario)"
            
            return "Variable/ID", "Objeto (vario)"

        elif tipo == "OP" and valor in ["[]"]:
            return "Literal", "Lista/Arreglo"
        
        return "Desconocido", "Error de Tipo"


    def mostrar_tabla(self, contenido):
        if not contenido.strip():
            messagebox.showwarning("Advertencia", "El área de texto está vacía.")
            return

        tokens = self.analizador_lexico.separar_token(contenido)

        simbolos_por_nombre = {}

        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token["tipo"] == "ID" and i + 1 < len(tokens) and tokens[i+1]["valor"] == "=":
                
                nombre = token["valor"]
                
                if i + 2 < len(tokens):
                    valor_token = tokens[i+2]
                    tipo_valor = valor_token["tipo"]
                    valor_valor = valor_token["valor"]
                    
                    categoria_valor, tipo_dato = self._obtener_tipo_y_categoria(tipo_valor, valor_valor)
                    
                    categoria_final, _ = self._obtener_tipo_y_categoria("ID", nombre)
                    
                    simbolos_por_nombre[nombre] = {
                        "nombre": nombre,
                        "categoria": categoria_final,
                        "tipo_dato": tipo_dato,
                        "valor": valor_valor.strip('"')
                    }
                    
                i += 3 
                continue 
            
            elif token["tipo"] == "PR" or token["tipo"] == "ID":
                nombre = token["valor"]
                
                if nombre not in simbolos_por_nombre: 
                    
                    categoria, tipo_dato = self._obtener_tipo_y_categoria(token["tipo"], nombre)

                    if "Función/Método" in categoria or "Estructura de Control" in categoria or token["tipo"] == "PR":
                        simbolos_por_nombre[nombre] = {
                            "nombre": nombre,
                            "categoria": categoria,
                            "tipo_dato": tipo_dato,
                            "valor": "-"
                        }

            i += 1
            
        simbolos = list(simbolos_por_nombre.values())
        
        ventana_tabla = tk.Toplevel(self.root)
        ventana_tabla.title("Tabla de Símbolos")
        ventana_tabla.geometry("950x400")
        
        columnas = ("Nombre del Símbolo", "Categoría", "Tipo de Dato", "Valor")
        tabla = ttk.Treeview(ventana_tabla, columns=columnas, show='headings')
        
        tabla.column("Nombre del Símbolo", anchor='center', width=200)
        tabla.column("Categoría", anchor='center', width=200)
        tabla.column("Tipo de Dato", anchor='center', width=200)
        tabla.column("Valor", anchor='center', width=150)
        
        for col in columnas:
            tabla.heading(col, text=col)
        
        tabla.pack(fill=tk.BOTH, expand=True)

        for simb in simbolos:
            tabla.insert("", tk.END, values=(
                simb["nombre"], simb["categoria"], simb["tipo_dato"], simb["valor"]
            ))

        scroll_y = ttk.Scrollbar(ventana_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscroll=scroll_y.set)
        scroll_y.pack(side="right", fill="y")