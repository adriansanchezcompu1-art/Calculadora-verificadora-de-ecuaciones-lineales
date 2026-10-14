"""Motor matematico: interpreta, resuelve y verifica ecuaciones.

No depende de la interfaz grafica, asi que se puede probar por separado.
"""

from .interprete import interpretar, interpretar_ecuacion, obtener_variables
from .resolver import resolver
from .verificador import verificar_solucion, verificar_pasos
