"""Verificacion de soluciones y de procedimientos paso a paso."""

import sympy as sp

from .interprete import interpretar, interpretar_ecuacion, obtener_variables


def verificar_solucion(ecuacion, nombre_variable, valor_texto):
    variables = obtener_variables(ecuacion)

    mapa = {v.name: v for v in variables}

    if nombre_variable not in mapa:
        raise ValueError(
            f"La variable {nombre_variable} no aparece en la ecuacion."
        )

    valor = interpretar(valor_texto)

    diferencia = sp.simplify(
        (ecuacion.lhs - ecuacion.rhs).subs(
            mapa[nombre_variable], valor
        )
    )

    if diferencia == 0:
        return (
            True,
            f"CORRECTO: {nombre_variable} = {sp.sstr(valor)} "
            "satisface la ecuacion."
        )

    return (
        False,
        "INCORRECTO: al sustituir el valor, "
        f"la diferencia es {sp.sstr(diferencia)}, no 0."
    )


def verificar_pasos(texto):
    lineas = [
        linea.strip()
        for linea in texto.splitlines()
        if linea.strip()
    ]

    if len(lineas) < 2:
        raise ValueError(
            "Escribe al menos la ecuacion inicial y un paso."
        )

    ecuaciones = []

    for numero, linea in enumerate(lineas, start=1):
        try:
            ecuaciones.append(
                interpretar_ecuacion(linea)
            )
        except ValueError as error:
            raise ValueError(
                f"Error en la linea {numero}: {error}"
            ) from error

    for i in range(len(ecuaciones) - 1):
        anterior = ecuaciones[i]
        siguiente = ecuaciones[i + 1]

        numero_paso = i + 2

        variables = sorted(
            anterior.free_symbols | siguiente.free_symbols,
            key=lambda s: s.name
        )

        if len(variables) != 1:
            return (
                False,
                f"Paso {numero_paso}: esta version solo "
                "compara ecuaciones con una variable."
            )

        x = variables[0]

        expresion_anterior = sp.expand(
            anterior.lhs - anterior.rhs
        )

        expresion_siguiente = sp.expand(
            siguiente.lhs - siguiente.rhs
        )

        try:
            polinomio_anterior = sp.Poly(
                expresion_anterior, x
            )
            polinomio_siguiente = sp.Poly(
                expresion_siguiente, x
            )
        except sp.PolynomialError:
            return (
                False,
                f"Paso {numero_paso}: no se pudo "
                "comprobar esta transformacion."
            )

        if (
            polinomio_anterior.degree() > 1
            or polinomio_siguiente.degree() > 1
        ):
            return (
                False,
                f"Paso {numero_paso}: el verificador "
                "admite por ahora ecuaciones lineales."
            )

        soluciones_anteriores = sp.solve(
            expresion_anterior, x
        )
        soluciones_siguientes = sp.solve(
            expresion_siguiente, x
        )

        conjunto_anterior = {
            sp.simplify(s) for s in soluciones_anteriores
        }

        conjunto_siguiente = {
            sp.simplify(s) for s in soluciones_siguientes
        }

        if conjunto_anterior != conjunto_siguiente:
            return (
                False,
                f"ERROR DETECTADO EN EL PASO {numero_paso}\n"
                f"La ecuacion anterior tiene las soluciones: "
                f"{soluciones_anteriores}\n"
                f"La nueva ecuacion tiene las soluciones: "
                f"{soluciones_siguientes}"
            )

    return (
        True,
        "PROCEDIMIENTO CORRECTO.\n"
        "Todos los pasos comprobados conservan la misma solucion."
    )
