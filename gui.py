import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

# GUI Principal
def crear_ventana_principal():
    # Cargar la imagen de fondo
    imagen_original = Image.open("assets/ying_yang.png")

    # Función al cerrado de ventana
    def on_closing():
        root.destroy()

    # Función para ajustar la imagen de fondo al tamaño de la ventana
    def ajustar_imagen(event):
        # Obtener las dimensiones de la ventana después de redimensionar
        window_width = event.width
        window_height = event.height

        # Escalar la imagen de fondo
        imagen_resized = imagen_original.resize((window_width, window_height), Image.BILINEAR)
        imagen_fondo = ImageTk.PhotoImage(imagen_resized)
        root.imagen_fondo = imagen_fondo
        # Actualizar la imagen en el widget Label
        label_fondo.config(image=imagen_fondo)
        label_fondo.image = imagen_fondo  # Mantener una referencia
    
    # Creacion de la ventana
    root = tk.Tk()


    # Escalar la imagen original para inicializar la imagen de fondo
    imagen_inicial = imagen_original.resize((680, 400), Image.BILINEAR)
    imagen_fondo = ImageTk.PhotoImage(imagen_inicial)

    #Mantenemos la referencia de la imagen para que no sea eliminada por el recolector de python
    root.imagen_fondo = imagen_fondo

    # Crear un label con la imagen de fondo
    label_fondo = tk.Label(root, image=imagen_fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

    # Configuramos el evento de cerrado de ventana
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Configurar el evento de redimensionamiento de la ventana
    root.bind("<Configure>", ajustar_imagen)

    
    

    # Tamaño de la ventana
    window_width = 680
    window_height = 400

    # Centrar la ventana en la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    root.title("Requenapp")

    # Tamaños máximos y mínimos de la ventana
    root.maxsize(1360, 800)
    root.minsize(680, 400)
    # Opacidad
    root.attributes("-alpha", 1) 
    # Icono de la ventana
    root.iconbitmap("assets/icon_root.ico")           

    # Crear una etiqueta e invocar su constructor pasando los atributos
    lbl_inicio = tk.Label(root, text= 'Bienvenido a Requenapp')
    lbl_inicio.config(font=("Times New Roman", 12), bg='white', fg='black')
    # Indicar que se muestre en la pantalla
    lbl_inicio.pack(pady=20)

    # Regresar la ventana principal
    return root


# Interfaz de selección de carpeta
def seleccionar_carpeta():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de tkinter

    carpeta = filedialog.askdirectory(title="Seleccionar carpeta")
    return carpeta

# Interfaz para seleccion de ubicacion y nombre de archivo
def solicitar_nombre_archivo_xlsx():
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana principal
    nombre_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    return nombre_archivo


def imprimir_alerta(text):
    tk.messagebox.showinfo("", text)
