import tkinter as tk
from tkinter import filedialog, messagebox

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz Gráfica")
        self.root.geometry("800x600")
        
        #--Configurar el menú principal
        self.crear_menu()
        
        # Crear las ventanas principales
        self.crear_ventanas()