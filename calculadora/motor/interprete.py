"""Convierte texto escrito por el usuario en expresiones de SymPy."""

import ast
import sympy as sp

OPERACIONES = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a ** b,
}


def interpretar(texto):
    """Convierte texto matematico en una expresion SymPy."""
    texto = texto.strip().replace("^", "**")

    if not texto:
        raise ValueError("Escribe una expresion.")

    try:
        arbol = ast.parse(texto, mode="eval")
    except SyntaxError as error:
        raise ValueError("La expresion tiene un formato incorrecto.") from error

    def convertir(nodo):
        if isinstance(nodo, ast.Expression):
            return convertir(nodo.body)

        if isinstance(nodo, ast.Constant):
            if isinstance(nodo.value, bool):
                raise ValueError("Valor no permitido.")

            if isinstance(nodo.value, int):
                return sp.Integer(nodo.value)

            if isinstance(nodo.value, float):
                return sp.Rational(str(nodo.value))

            raise ValueError("Solo se permiten numeros.")

        if isinstance(nodo, ast.Name):
            if nodo.id.startswith("_"):
                raise ValueError("Nombre de variable no permitido.")

            return sp.Symbol(nodo.id)

        if isinstance(nodo, ast.UnaryOp):
            valor = convertir(nodo.operand)

            if isinstance(nodo.op, ast.UAdd):
                return valor

            if isinstance(nodo.op, ast.USub):
                return -valor

            raise ValueError("Operador no permitido.")

        if isinstance(nodo, ast.BinOp):
            tipo = type(nodo.op)

            if tipo not in OPERACIONES:
                raise ValueError("Operador no permitido.")

            izquierda = convertir(nodo.left)
            derecha = convertir(nodo.right)

            if tipo is ast.Pow:
                if not derecha.is_Integer:
                    raise ValueError("Usa exponentes enteros.")

                if abs(int(derecha)) > 20:
                    raise ValueError("Exponente demasiado grande.")

            if tipo is ast.Div and derecha == 0:
                raise ValueError("No puedes dividir entre cero.")

            return OPERACIONES[tipo](izquierda, derecha)

        raise ValueError(
            "Usa numeros, variables, parentesis y operaciones basicas."
        )

    resultado = convertir(arbol)

    if resultado.is_commutative is not True:
        raise ValueError("Expresion no admitida.")

    return resultado


def interpretar_ecuacion(texto):
    """Interpreta una ecuacion escrita con un signo igual."""
    if texto.count("=") != 1:
        raise ValueError(
            "Escribe una ecuacion como 2*x + 5 = 15."
        )

    izquierda, derecha = texto.split("=")

    return sp.Eq(
        interpretar(izquierda),
        interpretar(derecha),
        evaluate=False
    )


def obtener_variables(ecuacion):
    """Devuelve las variables de la ecuacion ordenadas por nombre."""
    return sorted(ecuacion.free_symbols, key=lambda s: s.name)
