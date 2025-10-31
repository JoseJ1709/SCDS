"""
Método de Romberg para Integración Numérica
Usa extrapolación de Richardson sobre la regla del trapecio
"""

import numpy as np
import matplotlib.pyplot as plt


def romberg(f, a, b, n_max=10, tol=1e-8, mostrar_tabla=True):
    """
    Integración de Romberg

    Parámetros:
    -----------
    f : function
        Función a integrar
    a, b : float
        Límites de integración
    n_max : int
        Número máximo de niveles de refinamiento
    tol : float
        Tolerancia para detener (criterio de convergencia)
    mostrar_tabla : bool
        Si True, muestra la tabla de Romberg

    Retorna:
    --------
    I : float
        Aproximación de la integral
    R : matriz
        Tabla de Romberg completa
    """
    # Inicializar tabla de Romberg
    R = np.zeros((n_max, n_max))

    # Primera columna: Regla del trapecio con n = 1, 2, 4, 8, ...
    h = b - a
    R[0, 0] = h * (f(a) + f(b)) / 2  # Trapecio con n=1

    print("=" * 80)
    print("MÉTODO DE ROMBERG")
    print("=" * 80 + "\n")
    print(f"Integrando en [{a}, {b}]")
    print(f"Tolerancia: {tol:.2e}\n")

    # Construir tabla de Romberg
    for i in range(1, n_max):
        # Calcular R(i,0) usando la fórmula recursiva del trapecio
        h = h / 2  # h_i = h_{i-1} / 2
        suma = 0

        # Sumar puntos intermedios
        for k in range(1, 2 ** i, 2):
            x_k = a + k * h
            suma += f(x_k)

        # Fórmula recursiva: R(i,0) = R(i-1,0)/2 + h * suma
        R[i, 0] = R[i - 1, 0] / 2 + h * suma

        # Extrapolación de Richardson para columnas j > 0
        for j in range(1, i + 1):
            # Fórmula: R(i,j) = R(i,j-1) + [R(i,j-1) - R(i-1,j-1)] / (4^j - 1)
            R[i, j] = R[i, j - 1] + (R[i, j - 1] - R[i - 1, j - 1]) / (4 ** j - 1)

        # Criterio de parada: comparar R(i,i) con R(i-1,i-1)
        if i > 0 and abs(R[i, i] - R[i - 1, i - 1]) < tol:
            print(f"✅ Convergencia alcanzada en nivel {i}")
            if mostrar_tabla:
                mostrar_tabla_romberg(R, i)
            return R[i, i], R[:i + 1, :i + 1]

    print(f"⚠️  Se alcanzó el máximo de niveles ({n_max})")
    if mostrar_tabla:
        mostrar_tabla_romberg(R, n_max - 1)

    return R[n_max - 1, n_max - 1], R


def mostrar_tabla_romberg(R, n_filas):
    """
    Muestra la tabla de Romberg de forma legible
    """
    print("\n" + "=" * 80)
    print("TABLA DE ROMBERG")
    print("=" * 80 + "\n")

    # Encabezado
    print(f"{'i':<5}", end="")
    for j in range(n_filas + 1):
        print(f"{'R(i,' + str(j) + ')':<20}", end="")
    print("\n" + "-" * 80)

    # Datos
    for i in range(n_filas + 1):
        print(f"{i:<5}", end="")
        for j in range(i + 1):
            print(f"{R[i, j]:<20.12f}", end="")
        print()

    print("=" * 80)

    # Mostrar patrón de mejora
    print(f"\n📊 Análisis de convergencia:")
    print(f"{'Nivel':<10} {'R(i,i)':<20} {'Error estimado':<20}")
    print("-" * 50)

    for i in range(min(n_filas + 1, 8)):
        if i == 0:
            print(f"{i:<10} {R[i, i]:<20.12f} {'N/A':<20}")
        else:
            error_est = abs(R[i, i] - R[i - 1, i - 1])
            print(f"{i:<10} {R[i, i]:<20.12f} {error_est:<20.2e}")
