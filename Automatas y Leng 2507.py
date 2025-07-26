import tkinter as tk
from tkinter import filedialog, messagebox
#-- Comentoarios en naraja son explicacion de ayuda para saber que hace las cossas
#? Azul muestra mi logica para saber que hago 
class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz ")
        self.root.geometry("800x600")
        self.crear_menu()
    
    def crear_menu(self):
        menubar = tk.Menu(self.root)
        
        #-- Menú Archivo logica basada en word 
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Guardar", command=self.guardar)
        menu_archivo.add_command(label="Guardar como", command=self.guardar_como)
        #-- Line gis que aparece dividien cerra y guardar
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

# Ejecutar para probar
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
