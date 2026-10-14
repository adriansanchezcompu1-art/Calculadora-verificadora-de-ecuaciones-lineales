# Calculadora-verificadora-de-ecuaciones-lineales
Mi primer proyecto, apenas estoy aprendiendo sobre Python, espero la disfruten

Primer aplicación de escritorio seria de mi parte (contendra futuras actualizaciones)

#==========================#
            V1.0                             #14/10/2026#
#==========================#            

## capacidades
-Funciona como calculadora y verificadora de ecuaciones lineales (ejemplo: 2*x + 5= 15)
-Tiene zona de descomposición de ecuaciones
-Detectar en que paso de un procedimiento se encuentra un error
-Trabajar con + - * ^ / () 

## Cómo usarla
1. Instala las dependencias: `pip install sympy pillow`
2. Ejecuta: `python main.py`

## Estructura
- `motor/`: la parte matemática
- `interfaz/`: la ventana (tkinter)

## limitaciones conocidas
-Interfaz Arcaica
-No acepta la "," para numeros decimales (solo lee "." EJemplo: 2.2)
-Error a la hora de proponer un problema matemático son soluciones infinitas
-Todavia no cuenta con interpretador (escritura bastante estricta)
