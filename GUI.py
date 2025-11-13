import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext  
from tkinter import PhotoImage
import os
import tkinter.ttk as ttk  

from Clasificar import Separador_Lexico
from AFD import AFD_analizar
from TablaSimbolos import TablaSimbolos

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico y Sintáctico")
        self.root.geometry("1200x800")
        self.cargar_iconos()
        self.crear_menu1()
        self.crear_interfaz_principal()
        self.configurar_drag_drop() 
       

        # Inicializar  analizadores
        self.analizador_lexico = Separador_Lexico()
        self.analizador_sintactico = AFD_analizar()
        self.tabla_simbolos = TablaSimbolos(self.root)
        self.last_tokens = None 

        
    def cargar_iconos(self):
        try:
            self.icono_guardar = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\img\imgGuardar2.png').subsample(4, 4)
            self.icono_guardarComo = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\img\imgGuardar.png').subsample(4, 4)
            self.icono_cerrar = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\img\imgCerrar.png').subsample(4, 4)
            self.icono_abrir = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\img\imgOpen.png').subsample(50, 50)
            self.icono_analizar = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\img\imgAnalizar.png').subsample(20, 20)
            self.icono_sintactico = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\img\imgSintactico.png').subsample(20, 20)
            self.icono_limpiar = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\img\imglimpiar.png').subsample(4, 4)
        except:
            messagebox.showerror("Error", "No se pudieron cargar los iconos")

    def crear_menu1(self):
        menubar = tk.Menu(self.root)
       
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Abrir", command=self.abrir_archivo, image=self.icono_abrir, compound=tk.LEFT)
        menu_archivo.add_command(label="Guardar", command=self.guardar, image=self.icono_guardar, compound=tk.LEFT)
        menu_archivo.add_command(label="Guardar como", command=self.guardar_como, image=self.icono_guardarComo, compound=tk.LEFT)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Limpiar Todo", command=self.limpiar_todo, image=self.icono_limpiar, compound=tk.LEFT) 
        menu_archivo.add_command(label="Cerrar", command=self.cerrar, image=self.icono_cerrar, compound=tk.LEFT)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        # Menú Analizar con DOS OPCIONES
        menu_analizar = tk.Menu(menubar, tearoff=0)
        menu_analizar.add_command(label="Análisis Léxico", command=self.analizar_lexico, image=self.icono_analizar, compound=tk.LEFT)
        menu_analizar.add_command(label="Análisis Sintáctico", command=self.analizar_sintactico, image=self.icono_sintactico, compound=tk.LEFT)
        menubar.add_cascade(label="Analizar", menu=menu_analizar)
        


        menu_analizar.add_separator()
        menu_analizar.add_command(label="Tabla de Símbolos", command=self.mostrar_tabla_simbolos)
        self.root.config(menu=menubar)

    def crear_interfaz_principal(self):
        # Marco principal vertical
        self.marco_principal = tk.PanedWindow(self.root, orient=tk.VERTICAL, bg="#f0f0f0")
        self.marco_principal.pack(fill=tk.BOTH, expand=True)
        
        # Marco superior para las DOS ventanas
        self.marco_superior = tk.PanedWindow(self.marco_principal, orient=tk.HORIZONTAL, bg="#f0f0f0")
        
        # Ventana 1 
        self.ventana1 = tk.LabelFrame(
            self.marco_superior, 
            text="Código Fuente", 
            padx=4, 
            pady=4,
            bg="white",
            font=('Arial', 10, 'bold')
        )
        self.scroll_text1 = scrolledtext.ScrolledText(
            self.ventana1,
            wrap=tk.WORD,
            width=40,
            height=20,
            font=('Consolas', 11),
            bg="white",
            fg="black"
        )
        self.scroll_text1.pack(fill=tk.BOTH, expand=True)
        
        # Ventana 2 - Tokens
        self.ventana2 = tk.LabelFrame(
            self.marco_superior,
            text="Tokens Identificados",
            padx=4,
            pady=4,
            bg="white",
            font=('Arial', 10, 'bold')
        )
        self.scroll_text2 = scrolledtext.ScrolledText(
            self.ventana2,
            wrap=tk.WORD,
            width=40,
            height=20,
            font=('Consolas', 11),
            bg="white",
            fg="black"
        )
        self.scroll_text2.pack(fill=tk.BOTH, expand=True)
        
        # Agregar las dos ventanas al marco superior
        self.marco_superior.add(self.ventana1)
        self.marco_superior.add(self.ventana2)
        
        # Ventana de errores sintacticos
        self.terminal = tk.LabelFrame(
            self.marco_principal,
            text="Errores Sintácticos",
            padx=4,
            pady=4,
            bg="white",
            fg="black",
            font=('Arial', 10, 'bold')
        )
        self.terminal_text = scrolledtext.ScrolledText(
            self.terminal,
            wrap=tk.WORD,
            width=80,
            height=10,
            font=('Consolas', 10),
            bg="white",
            fg="black",
            insertbackground="black"
        )
        self.terminal_text.pack(fill=tk.BOTH, expand=True)
        
        # Agregar todo al marco principal
        self.marco_principal.add(self.marco_superior)
        self.marco_principal.add(self.terminal)
        
        # Configurar tamaños
        self.marco_principal.paneconfig(self.marco_superior, minsize=400)
        self.marco_principal.paneconfig(self.terminal, minsize=200)

    
    def mostrar_tabla_simbolos(self):
      #? Comprobacion
        if self.last_tokens is None:
            messagebox.showwarning("Advertencia", "Debe ejecutar primero el Análisis Léxico o Sintáctico para generar la Tabla de Símbolos.")
            return

        # Llama a mostrar_tabla  
        self.tabla_simbolos.mostrar_tabla(self.last_tokens)


    # ------------------ Análisis Léxico ------------------
    def analizar_lexico(self):
        contenido = self.scroll_text1.get('1.0', tk.END).strip()
        if not contenido:
            messagebox.showwarning("Advertencia", "El área de texto está vacía.")
            return
        try:
            tokens = self.analizador_lexico.separar_token(contenido)
            self.last_tokens = tokens 
            # Mostrar tokens en Ventana 2
            resultado_tokens = ""
            linea_actual = 0
            for token in tokens:
                if token['linea'] != linea_actual:
                    if linea_actual != 0:
                        resultado_tokens += "\n"
                    resultado_tokens += f"L{token['linea']}: "
                    linea_actual = token['linea']
                resultado_tokens += f"{token['tipo']}({token['valor']}) "
            self.scroll_text2.delete('1.0', tk.END)
            self.scroll_text2.insert(tk.END, resultado_tokens)
            
            self.terminal_text.delete('1.0', tk.END)
            messagebox.showinfo("Análisis Léxico", f"Se identificaron {len(tokens)} tokens")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo analizar el texto: {str(e)}")
            self.terminal_text.delete('1.0', tk.END)
            self.terminal_text.insert(tk.END, f"Error: {str(e)}\n")

    # ------------------ Análisis Sintáctico ------------------
    def analizar_sintactico(self):
        contenido = self.scroll_text1.get('1.0', tk.END).strip()
        if not contenido:
            messagebox.showwarning("Advertencia", "El área de texto está vacía.")
            return
        try:
            #  Separar tokens
            tokens = self.analizador_lexico.separar_token(contenido)
            self.last_tokens = tokens # NUEVO: Guarda los tokens
            
            # Analizar sintaxis
            errores = self.analizador_sintactico.analizar_sintaxis(tokens)
            
            # Mostrar tokens en Ventana 2
            resultado_tokens = ""
            linea_actual = 0
            for token in tokens:
                if token['linea'] != linea_actual:
                    if linea_actual != 0:
                        resultado_tokens += "\n"
                    resultado_tokens += f"L{token['linea']}: "
                    linea_actual = token['linea']
                resultado_tokens += f"{token['tipo']}({token['valor']}) "
            self.scroll_text2.delete('1.0', tk.END)
            self.scroll_text2.insert(tk.END, resultado_tokens)
            
            #  Mostrar errores
            self.terminal_text.delete('1.0', tk.END)
            if errores:
                for e in errores:
                    self.terminal_text.insert(tk.END, e + "\n")
            else:
                self.terminal_text.insert(tk.END, "No se encontraron errores sintácticos.")

    
            messagebox.showinfo("Análisis Sintáctico",
                                f"Tokens identificados: {len(tokens)}\nErrores: {len(errores)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo analizar el texto: {str(e)}")
            self.terminal_text.delete('1.0', tk.END)
            self.terminal_text.insert(tk.END, f"Error: {str(e)}\n")

    # ------------------ Métodos del menú Archivo ------------------
    def abrir_archivo(self, event=None):
        file_path = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    contenido = file.read()
                    self.scroll_text1.delete('1.0', tk.END)
                    self.scroll_text1.insert(tk.END, contenido)
                    self.scroll_text2.delete('1.0', tk.END)
                    self.terminal_text.delete('1.0', tk.END)
                #? Reset lo de la tabla
                    self.last_tokens = None 
                    messagebox.showinfo("Éxito", f"Archivo cargado: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{str(e)}")

    def guardar(self):
        messagebox.showinfo("Guardar", "Función Guardar en desarrollo")

    def guardar_como(self):
        file = filedialog.asksaveasfilename()
        if file:
            try:
                contenido = self.scroll_text1.get('1.0', tk.END)
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                messagebox.showinfo("Guardar como", f"Archivo guardado como: {file}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
        
    def cerrar(self):
        if messagebox.askokcancel("Cerrar", "¿Está seguro que desea cerrar la aplicación?"):
            self.root.destroy()

    def configurar_drag_drop(self):
        self.scroll_text1.bind('<Double-Button-1>', self.abrir_archivo)


        #--- Limiar
    def limpiar_todo(self):
        """Limpia todos los campos de texto y resetea los analizadores"""
        respuesta = messagebox.askyesno(
        "Limpiar Todo", 
        "¿Confirma limpieza?"
        )
    
        if respuesta:
        
            self.scroll_text1.delete('1.0', tk.END)  
            self.scroll_text2.delete('1.0', tk.END) 
            self.terminal_text.delete('1.0', tk.END)  
            #lo de la tabla
            self.last_tokens = None 
        
        
            self.analizador_lexico = Separador_Lexico()  
            self.analizador_sintactico = AFD_analizar()
        
        
           

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()