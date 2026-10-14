"""Ventana principal de la calculadora."""

import tkinter as tk
from tkinter import ttk

import sympy as sp

from motor import (
    interpretar_ecuacion,
    resolver,
    verificar_solucion,
    verificar_pasos,
)


class Calculadora(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Calculadora Matematica (by Alexander)")
        self.geometry("780x720")
        self.minsize(650, 600)

        self.configure(bg="#F1F5F9")

        estilo = ttk.Style(self)

        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure(
            "Titulo.TLabel",
            font=("Segoe UI", 19, "bold"),
            background="#F1F5F9"
        )

        estilo.configure(
            "TButton",
            padding=8
        )

        contenedor = ttk.Frame(self, padding=18)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor,
            text="Calculadora / Verificadora",
            style="Titulo.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            contenedor,
            text="Resuelve ecuaciones y comprueba procedimientos."
        ).pack(anchor="w", pady=(4, 14))

        # Panel de ecuaciones
        panel = ttk.LabelFrame(
            contenedor,
            text="Resolver una ecuacion (RESPETAR FORMATO DE ESCRITURA)",
            padding=12
        )
        panel.pack(fill="x", pady=(0, 12))

        ttk.Label(
            panel,
            text="Ecuacion (ejemplo: 2*x + 5 = 15)"
        ).pack(anchor="w")

        self.entrada_ecuacion = ttk.Entry(
            panel,
            font=("Consolas", 12)
        )
        self.entrada_ecuacion.pack(
            fill="x", pady=(5, 10)
        )
        self.entrada_ecuacion.insert(
            0, "2*x + 5 = 15"
        )

        ttk.Button(
            panel,
            text="Resolver ecuacion",
            command=self.accion_resolver
        ).pack(fill="x", pady=(0, 10))

        fila = ttk.Frame(panel)
        fila.pack(fill="x")

        ttk.Label(
            fila, text="Variable:"
        ).pack(side="left")

        self.entrada_variable = ttk.Entry(
            fila, width=8
        )
        self.entrada_variable.insert(0, "x")
        self.entrada_variable.pack(
            side="left", padx=(6, 15)
        )

        ttk.Label(
            fila, text="Valor:"
        ).pack(side="left")

        self.entrada_valor = ttk.Entry(
            fila, width=12
        )
        self.entrada_valor.insert(0, "5")
        self.entrada_valor.pack(
            side="left", padx=6
        )

        ttk.Button(
            fila,
            text="Verificar valor",
            command=self.accion_verificar
        ).pack(side="left", padx=(8, 0))

        # Panel de procedimientos
        panel_pasos = ttk.LabelFrame(
            contenedor,
            text="Verificar procedimiento",
            padding=12
        )
        panel_pasos.pack(
            fill="both", expand=True, pady=(0, 12)
        )

        ttk.Label(
            panel_pasos,
            text="Escribe cada paso en una linea distinta:"
        ).pack(anchor="w")

        self.entrada_pasos = tk.Text(
            panel_pasos,
            height=7,
            font=("Consolas", 11),
            wrap="word"
        )
        self.entrada_pasos.pack(
            fill="both", expand=True, pady=8
        )

        self.entrada_pasos.insert(
            "1.0",
            "2*x + 5 = 15\n"
            "2*x = 10\n"
            "x = 5"
        )

        ttk.Button(
            panel_pasos,
            text="Verificar procedimiento",
            command=self.accion_pasos
        ).pack(anchor="e")

        # Panel de resultados
        panel_resultado = ttk.LabelFrame(
            contenedor,
            text="Resultado",
            padding=10
        )
        panel_resultado.pack(fill="x")

        self.resultado = tk.Text(
            panel_resultado,
            height=6,
            wrap="word",
            font=("Segoe UI", 10),
            state="disabled"
        )
        self.resultado.pack(fill="x")

        self.mostrar(
            "Listo. Introduce una ecuacion para comenzar."
        )

        ttk.Label(
            contenedor,
            text="Usa * para multiplicar y ^ o ** para potencias."
        ).pack(anchor="w", pady=(10, 0))

    def mostrar(self, mensaje):
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", mensaje)
        self.resultado.configure(state="disabled")

    def accion_resolver(self):
        try:
            ecuacion = interpretar_ecuacion(
                self.entrada_ecuacion.get()
            )

            respuesta = resolver(ecuacion)

            self.mostrar(
                f"Ecuacion: {sp.sstr(ecuacion.lhs)} = "
                f"{sp.sstr(ecuacion.rhs)}\n\n"
                f"{respuesta}"
            )

        except Exception as error:
            self.mostrar(f"No se pudo resolver:\n{error}")

    def accion_verificar(self):
        try:
            ecuacion = interpretar_ecuacion(
                self.entrada_ecuacion.get()
            )

            variable = self.entrada_variable.get().strip()
            valor = self.entrada_valor.get()

            correcto, mensaje = verificar_solucion(
                ecuacion, variable, valor
            )

            self.mostrar(mensaje)

        except Exception as error:
            self.mostrar(
                f"No se pudo verificar:\n{error}"
            )

    def accion_pasos(self):
        try:
            texto = self.entrada_pasos.get(
                "1.0", "end"
            )

            correcto, mensaje = verificar_pasos(texto)

            self.mostrar(mensaje)

        except Exception as error:
            self.mostrar(
                f"No se pudo verificar:\n{error}"
            )
