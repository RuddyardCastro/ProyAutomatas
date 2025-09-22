10  

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext  
from tkinter import PhotoImage
import os
#-- Comentoarios en naraja son explicacion de ayuda para saber que hace las cossas
#? Azul muestra mi logica para saber que hago 
class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz ")
        self.root.geometry("1060x1060")
        self.cargar_iconos()
        self.crear_menu1()
        self.crear_marco_principal()


    def cargar_iconos(self):
       
       
            #-- Como dato por alguna razon los iconos a mas grande numerov mas pequeños
           self.icono_guardar = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\imgGuardar2.png').subsample(4, 4)
           self.icono_guardarComo = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\imgGuardar.png').subsample(4, 4)
           self.icono_cerrar = PhotoImage(file=r'C:\Users\Ruddyard\Desktop\ProyEnGit\imgCerrar.png').subsample(4, 4)
            

    def crear_menu1(self):
        menubar = tk.Menu(self.root)
        
        #-- Menú Archivo logica basada en word 
        menu_archivo = tk.Menu(menubar, tearoff=0)

        
        menu_archivo.add_command(label="Guardar", command=self.guardar,image=self.icono_guardar,compound=tk.LEFT)
        menu_archivo.add_command(label="Guardar como", command=self.guardar_como,image=self.icono_guardarComo,compound=tk.LEFT)
        #-- Line gis que aparece dividien cerra y guardar
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Cerrar", command=self.cerrar,image=self.icono_cerrar,compound=tk.LEFT)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)



        #? Las funciones de guardar guardar como y cerrar se definen abajo para poder tener sepradao los nombre la parte grafica de las funciones 
        self.root.config(menu=menubar)

    def crear_menu2(self):
        menubar = tk.Menu(self.root)
        #? Esta es la copia que se va usar despues para las acciones 
        #-- Menú Archivo logica basada en word 
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Guardar", command=self.guardar)
        menu_archivo.add_command(label="Guardar como", command=self.guardar_como)
        #-- Linea gris que aparece dividien cerra y guardar
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Cerrar", command=self.cerrar)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        #? Las funciones de guardar guardar como y cerrar se definen abajo para poder tener sepradao los nombre la parte grafica de las funciones 
        self.root.config(menu=menubar)






    #? Aqui estan las funciones de los nombre que se miran en pantalla 
    def guardar(self):
        messagebox.showinfo("Guardar", "Función Guardar ")
    #-- Asksavedile es lo que me permite guardar en done io quiero 
    def guardar_como(self):
        file = filedialog.asksaveasfilename()
        if file:
            messagebox.showinfo("Guardar como", f"Archivo se guardará como: {file}")
        
    def cerrar(self):
        if messagebox.askokcancel("Cerrar", "¿Está seguro que desea cerrar la aplicación?"):
            #? Creo que breack no funciona a qui por ser visual no no un funcion 
            self.root.destroy()


    def crear_marco_principal(self):
    
    # --Marco principal 
        self.marco_principal = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#f0f0f0")
        self.marco_principal.pack(fill=tk.BOTH, expand=True)
    
    # --- VENTANA 1  ---
        self.ventana1 = tk.LabelFrame(
        self.marco_principal, 
        text="Ventana 1", 
        #-- El pad es el que mueve espacios entere las ventanas  
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
    
    # --- VENTANA 2 (Donde se va a ver el archivo despues ) ---
    #? El lable Frame es el que se mira arriba lo uso para diferencianr ventanas 
    #? Este borde no mas es estetica ya que no ayuda se sustituya por el elble celeste proyecto autmatas 
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
    
    # ? Utiliz self que segun entiendo es lo que permite decir a que marco se va incorporar 
    #? marco principal se le llamo al cuador donde esta archivo 
        self.marco_principal.add(self.ventana1)
        self.marco_principal.add(self.ventana2)
    
    
        self.marco_principal.paneconfig(self.ventana1, minsize=400)
        self.marco_principal.paneconfig(self.ventana2, minsize=400)
       
      
       
      


# Ejecutar para probar
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
#!Debe abrir y guradar las ventanas  agregar iconos  la otra versin de archivos es token indetificar clasificar ademas de cargar un archivo .py