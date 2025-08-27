import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext  
from tkinter import PhotoImage
import os

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz ")
        self.root.geometry("1060x1060")
        self.cargar_iconos()
        self.crear_menu1()
        self.crear_marco_principal()
        self.configurar_drag_drop() 
#-- Modificar las imagenes 
    def cargar_iconos(self):
        try:
            self.icono_guardar = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\img\imgGuardar2.png').subsample(4, 4)
            self.icono_guardarComo = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\img\imgGuardar.png').subsample(4, 4)
            self.icono_cerrar = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\img\imgCerrar.png').subsample(4, 4)
            self.icono_abrir = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\img\imgOpen.png').subsample(50, 50)
        except:
            messagebox.showerror("Error", "No se pudieron cargar los iconos")

            
#-- Botones elementos graficos 
    def crear_menu1(self):
        menubar = tk.Menu(self.root)
        
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Guardar", command=self.guardar, image=self.icono_guardar, compound=tk.LEFT)
        menu_archivo.add_command(label="Guardar como", command=self.guardar_como, image=self.icono_guardarComo, compound=tk.LEFT)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Cerrar", command=self.cerrar, image=self.icono_cerrar, compound=tk.LEFT)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        
        # Menú Analizar con opción Seleccionar
        menu_analizar = tk.Menu(menubar, tearoff=0)
        menu_analizar.add_command(label="Seleccionar", command=self.seleccionar)
        menubar.add_cascade(label="Analizar", menu=menu_analizar)
        
        menu_archivo.insert_command(0, label="Abrir", command=self.abrir_archivo ,image=self.icono_abrir, compound=tk.LEFT  )



    #-- Funciones de las acciones den el menu     
        self.root.config(menu=menubar)
    def guardar(self):
        messagebox.showinfo("Guardar", "Función Guardar ")

    def guardar_como(self):
        file = filedialog.asksaveasfilename()
        if file:
            messagebox.showinfo("Guardar como", f"Archivo se guardará como: {file}")
        
    def cerrar(self):
        if messagebox.askokcancel("Cerrar", "¿Está seguro que desea cerrar la aplicación?"):
            self.root.destroy()
    def seleccionar(self):
        # Función vacía para la opción Seleccionar (sin acción)
        pass
#  * aqui se modifica el abrir de archivo  
    def configurar_drag_drop(self):
       
        self.scroll_text1.bind('<Double-Button-1>', self.abrir_archivo)
       
        self.scroll_text2.bind('<Double-Button-1>', self.abrir_archivo)

    def abrir_archivo(self, event=None):
       
        file_path = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    contenido = file.read()
                   
                    if event and event.widget == self.scroll_text2:
                        self.scroll_text2.delete('1.0', tk.END)
                        self.scroll_text2.insert(tk.END, contenido)
                    else:
                        self.scroll_text1.delete('1.0', tk.END)
                        self.scroll_text1.insert(tk.END, contenido)
                        
                    messagebox.showinfo("Éxito", f"Archivo cargado: {os.path.basename(file_path)}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{str(e)}")
    #? ---------------------Crecion de los componentes fisicos -------------------------------------------
    def crear_marco_principal(self):
        # -- Marco principal 
        self.marco_principal = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#f0f0f0")
        self.marco_principal.pack(fill=tk.BOTH, expand=True)
    
        # --- VENTANA 1 (Editor de texto) ---
        self.ventana1 = tk.LabelFrame(
            self.marco_principal, 
            text="Ventana 1", 
            padx=4, 
            pady=4,
            bg="white"
        )
    
        self.scroll_text1 = scrolledtext.ScrolledText(
            self.ventana1,
            wrap=tk.WORD,
            width=40,
            height=40,
            font=('Arial', 10),
            bg="#f9f9f9"
        )
        self.scroll_text1.pack(fill=tk.BOTH, expand=True)
    
        # --- VENTANA 2 ---
        self.ventana2 = tk.LabelFrame(
            self.marco_principal,
            text="Ventana 2",
            padx=4,
            pady=4,
            bg="Blue"
        )
    
        self.scroll_text2 = scrolledtext.ScrolledText(
            self.ventana2,
            wrap=tk.WORD,
            width=200,
            height=200,
            font=('Arial', 10),
            bg="#f9f9f9"
        )
        self.scroll_text2.pack(fill=tk.BOTH, expand=True)
    
        self.marco_principal.add(self.ventana1)
        self.marco_principal.add(self.ventana2)
    #-- Modfifcar el tamaño de las ventanas 
        self.marco_principal.paneconfig(self.ventana1, minsize=400)
        self.marco_principal.paneconfig(self.ventana2, minsize=400)


    


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()