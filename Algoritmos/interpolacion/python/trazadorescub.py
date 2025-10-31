"""
Trazadores Cúbicos (Cubic trazadores_cubicoss)
Interpolación suave usando polinomios cúbicos por segmentos
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg


def trazadores_cubicos_naturales(xi, yi):
    """
    Calcula trazadores cúbicos con condiciones naturales (S''(x0) = S''(xn) = 0)

    Parámetros:
    -----------
    xi : array
        Puntos x conocidos (deben estar ordenados)
    yi : array
        Valores y conocidos

    Retorna:
    --------
    coeficientes : array
        Matriz (n-1) x 4 con coeficientes [a, b, c, d] de cada segmento
        S_i(x) = a_i + b_i(x-xi) + c_i(x-xi)^2 + d_i(x-xi)^3
    """
    xi = np.array(xi, dtype=float)
    yi = np.array(yi, dtype=float)
    n = len(xi)

    # Diferencias
    h = np.diff(xi)  # h[i] = xi[i+1] - xi[i]

    # Sistema tridiagonal para encontrar c[i] = S''(xi)/2
    # A * c = b
    A = np.zeros((n, n))
    b = np.zeros(n)

    # Condiciones naturales: S''(x0) = S''(xn) = 0
    A[0, 0] = 1
    A[n - 1, n - 1] = 1
    b[0] = 0
    b[n - 1] = 0

    # Ecuaciones internas
    for i in range(1, n - 1):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        b[i] = 3 * ((yi[i + 1] - yi[i]) / h[i] - (yi[i] - yi[i - 1]) / h[i - 1])

    # Resolver sistema
    c = linalg.solve(A, b)

    # Calcular coeficientes a, b, d
    a = yi[:-1].copy()
    b = np.zeros(n - 1)
    d = np.zeros(n - 1)

    for i in range(n - 1):
        b[i] = (yi[i + 1] - yi[i]) / h[i] - h[i] * (2 * c[i] + c[i + 1]) / 3
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])

    c = c[:-1]

    # Retornar como matriz (n-1) x 4
    coeficientes = np.column_stack([a, b, c, d])

    return coeficientes


def trazadores_cubicos_sujetos(xi, yi, dy0, dyn):
    """
    Calcula trazadores cúbicos con condiciones sujetas (derivadas en extremos)

    Parámetros adicionales:
    -----------------------
    dy0 : float
        Derivada en x0: S'(x0) = dy0
    dyn : float
        Derivada en xn: S'(xn) = dyn
    """
    xi = np.array(xi, dtype=float)
    yi = np.array(yi, dtype=float)
    n = len(xi)

    h = np.diff(xi)

    # Sistema tridiagonal
    A = np.zeros((n, n))
    b = np.zeros(n)

    # Condiciones sujetas en los extremos
    A[0, 0] = 2 * h[0]
    A[0, 1] = h[0]
    b[0] = 3 * ((yi[1] - yi[0]) / h[0] - dy0)

    A[n - 1, n - 2] = h[n - 2]
    A[n - 1, n - 1] = 2 * h[n - 2]
    b[n - 1] = 3 * (dyn - (yi[n - 1] - yi[n - 2]) / h[n - 2])

    # Ecuaciones internas
    for i in range(1, n - 1):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        b[i] = 3 * ((yi[i + 1] - yi[i]) / h[i] - (yi[i] - yi[i - 1]) / h[i - 1])

    # Resolver
    c = linalg.solve(A, b)

    # Calcular otros coeficientes
    a = yi[:-1].copy()
    b_coef = np.zeros(n - 1)
    d = np.zeros(n - 1)

    for i in range(n - 1):
        b_coef[i] = (yi[i + 1] - yi[i]) / h[i] - h[i] * (2 * c[i] + c[i + 1]) / 3
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])

    c = c[:-1]

    coeficientes = np.column_stack([a, b_coef, c, d])

    return coeficientes


def evaluar_trazadores_cubicos(xi, coeficientes, x):
    """
    Evalúa el trazadores_cubicos en el punto(s) x

    Parámetros:
    -----------
    xi : array
        Puntos de los nodos
    coeficientes : array
        Matriz (n-1) x 4 con coeficientes
    x : float o array
        Punto(s) donde evaluar
    """
    xi = np.array(xi)
    x = np.array(x)
    scalar_input = np.isscalar(x)
    x = np.atleast_1d(x)

    resultado = np.zeros_like(x, dtype=float)

    for idx, x_val in enumerate(x):
        # Encontrar el intervalo correcto
        if x_val <= xi[0]:
            i = 0
        elif x_val >= xi[-1]:
            i = len(xi) - 2
        else:
            i = np.searchsorted(xi, x_val) - 1
            i = min(i, len(coeficientes) - 1)

        # Evaluar S_i(x) = a + b(x-xi) + c(x-xi)^2 + d(x-xi)^3
        dx = x_val - xi[i]
        a, b, c, d = coeficientes[i]
        resultado[idx] = a + b * dx + c * dx ** 2 + d * dx ** 3

    return resultado[0] if scalar_input else resultado


def derivada_trazadores_cubicos(xi, coeficientes, x):
    """
    Calcula la derivada del trazadores_cubicos en x
    S'(x) = b + 2c(x-xi) + 3d(x-xi)^2
    """
    xi = np.array(xi)
    x = np.array(x)
    scalar_input = np.isscalar(x)
    x = np.atleast_1d(x)

    resultado = np.zeros_like(x, dtype=float)

    for idx, x_val in enumerate(x):
        if x_val <= xi[0]:
            i = 0
        elif x_val >= xi[-1]:
            i = len(xi) - 2
        else:
            i = np.searchsorted(xi, x_val) - 1
            i = min(i, len(coeficientes) - 1)

        dx = x_val - xi[i]
        a, b, c, d = coeficientes[i]
        resultado[idx] = b + 2 * c * dx + 3 * d * dx ** 2

    return resultado[0] if scalar_input else resultado


def segunda_derivada_trazadores_cubicos(xi, coeficientes, x):
    """
    Calcula la segunda derivada del trazadores_cubicos en x
    S''(x) = 2c + 6d(x-xi)
    """
    xi = np.array(xi)
    x = np.array(x)
    scalar_input = np.isscalar(x)
    x = np.atleast_1d(x)

    resultado = np.zeros_like(x, dtype=float)

    for idx, x_val in enumerate(x):
        if x_val <= xi[0]:
            i = 0
        elif x_val >= xi[-1]:
            i = len(xi) - 2
        else:
            i = np.searchsorted(xi, x_val) - 1
            i = min(i, len(coeficientes) - 1)

        dx = x_val - xi[i]
        a, b, c, d = coeficientes[i]
        resultado[idx] = 2 * c + 6 * d * dx

    return resultado[0] if scalar_input else resultado


def mostrar_coeficientes_trazadores_cubicos(xi, coeficientes):
    """
    Muestra los coeficientes de cada segmento del trazadores_cubicos
    """
    print("\nCoeficientes de los Trazadores Cúbicos:")
    print("=" * 80)
    print(f"{'Segmento':<15} {'Intervalo':<20} {'a':<12} {'b':<12} {'c':<12} {'d':<12}")
    print("-" * 80)

    for i in range(len(coeficientes)):
        a, b, c, d = coeficientes[i]
        intervalo = f"[{xi[i]:.2f}, {xi[i + 1]:.2f}]"
        print(f"S_{i}(x){'':<8} {intervalo:<20} {a:<12.6f} {b:<12.6f} {c:<12.6f} {d:<12.6f}")

    print("=" * 80)

    print("\nEcuaciones de cada segmento:")
    for i in range(len(coeficientes)):
        a, b, c, d = coeficientes[i]
        print(f"S_{i}(x) = {a:.6f} {b:+.6f}(x-{xi[i]:.2f}) {c:+.6f}(x-{xi[i]:.2f})² {d:+.6f}(x-{xi[i]:.2f})³")

