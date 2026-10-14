"""Resolucion de ecuaciones."""

import sympy as sp

from .interprete import obtener_variables


def resolver(ecuacion):
    variables = obtener_variables(ecuacion)

    if len(variables) == 0:
        diferencia = sp.simplify(
            ecuacion.lhs - ecuacion.rhs
        )

        if diferencia == 0:
            return "La igualdad es verdadera."

        return "La igualdad es falsa: no tiene solucion."

    if len(variables) > 1:
        return (
            "Esta version resuelve una variable a la vez. "
            "Variables encontradas: "
            + ", ".join(str(v) for v in variables)
        )

    variable = variables[0]

    soluciones = sp.solve(
        ecuacion.lhs - ecuacion.rhs,
        variable
    )

    if not soluciones:
        return "La ecuacion no tiene soluciones."

    if len(soluciones) == 1:
        return f"{variable} = {sp.sstr(soluciones[0])}"

    resultados = [
        f"{variable} = {sp.sstr(solucion)}"
        for solucion in soluciones
    ]

    return "Soluciones:\n" + "\n".join(resultados)
