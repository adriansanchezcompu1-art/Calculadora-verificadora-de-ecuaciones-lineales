"""Pantalla de bienvenida y arranque de la aplicacion."""

import tkinter as tk
from tkinter import ttk
from pathlib import Path

from PIL import Image, ImageTk

from .ventana import Calculadora

# El logo vive en la carpeta principal del proyecto (junto a main.py)
RUTA_LOGO = Path(__file__).resolve().parent.parent / "logo.png"


def iniciar_aplicacion():
    # Crear la calculadora, pero mantenerla oculta al inicio
    app = Calculadora()
    app.withdraw()

    # Crear la ventana de bienvenida
    bienvenida = tk.Toplevel(app)
    bienvenida.title("Fox Programmer")
    bienvenida.configure(bg="#101522")
    bienvenida.resizable(False, False)

    # Centrar la ventana
    ancho, alto = 500, 350
    x = (bienvenida.winfo_screenwidth() - ancho) // 2
    y = (bienvenida.winfo_screenheight() - alto) // 2
    bienvenida.geometry(f"{ancho}x{alto}+{x}+{y}")

    # Evitar que la ventana se cierre accidentalmente
    bienvenida.protocol("WM_DELETE_WINDOW", app.destroy)

    # Mostrar la ventana antes de cargar la imagen
    bienvenida.update_idletasks()

    print("Ruta del logo:", RUTA_LOGO)
    print("¿Existe el logo?:", RUTA_LOGO.exists())

    # Cargar y mostrar el logo
    try:
        imagen = Image.open(RUTA_LOGO).convert("RGBA")
        imagen.thumbnail((220, 170))

        # IMPORTANTE: asignar la ventana como master
        logo = ImageTk.PhotoImage(imagen, master=bienvenida)

        etiqueta_logo = tk.Label(
            bienvenida,
            image=logo,
            bg="#101522"
        )
        etiqueta_logo.image = logo
        etiqueta_logo.pack(pady=(25, 10))

    except Exception as error:
        print("Error al cargar el logo:", error)

        tk.Label(
            bienvenida,
            text="FOX PROGRAMMER",
            font=("Segoe UI", 24, "bold"),
            bg="#101522",
            fg="#76D7FF"
        ).pack(pady=(55, 20))

    # Nombre y descripción de la aplicación
    tk.Label(
        bienvenida,
        text="Calculadora matemática",
        font=("Segoe UI", 17, "bold"),
        bg="#101522",
        fg="white"
    ).pack(pady=8)

    tk.Label(
        bienvenida,
        text="Proyecto Escolar",
        font=("Segoe UI", 10),
        bg="#101522",
        fg="#A9B8D0"
    ).pack(pady=5)

    # Barra de carga
    barra = ttk.Progressbar(
        bienvenida,
        mode="indeterminate",
        length=220
    )
    barra.pack(pady=15)
    barra.start(12)

    # Abrir la calculadora después de 3 segundos
    def abrir_calculadora():
        barra.stop()
        bienvenida.destroy()
        app.deiconify()
        app.lift()
        app.focus_force()

    bienvenida.after(3000, abrir_calculadora)

    # Iniciar el bucle principal de Tkinter
    app.mainloop()
