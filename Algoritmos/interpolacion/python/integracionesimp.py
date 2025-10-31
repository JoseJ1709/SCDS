"""
Regla de Simpson 1/3 para Integración Numérica
Aproxima el área usando parábolas
"""

import numpy as np
import matplotlib.pyplot as plt


def simpson_1_3_simple(f, a, b):
    """
    Regla de Simpson 1/3 simple (una parábola)

    Fórmula: ∫[a,b] f(x)dx ≈ (b-a)/6 * [f(a) + 4*f((a+b)/2) + f(b)]

    Parámetros:
    -----------
    f : function
        Función a integrar
    a, b : float
        Límites de integración

    Retorna:
    --------
    I : float
        Aproximación de la integral
    """
    h = (b - a) / 2
    c = (a + b) / 2
    I = (h / 3) * (f(a) + 4*f(c) + f(b))
    return I


def simpson_1_3_compuesto(f, a, b, n):
    """
    Regla de Simpson 1/3 compuesto

    IMPORTANTE: n debe ser PAR

    Fórmula: I ≈ h/3 * [f(x0) + 4*f(x1) + 2*f(x2) + 4*f(x3) + ... + f(xn)]

    Parámetros:
    -----------
    f : function
        Función a integrar
    a, b : float
        Límites de integración
    n : int
        Número de subintervalos (DEBE SER PAR)

    Retorna:
    --------
    I : float
        Aproximación de la integral
    x : array
        Puntos de evaluación
    """
    if n % 2 != 0:
        raise ValueError("n debe ser par para Simpson 1/3")

    # Generar puntos
    x = np.linspace(a, b, n+1)
    h = (b - a) / n

    # Evaluar función
    y = f(x)

    # Fórmula de Simpson 1/3
    # Suma con pesos: 1, 4, 2, 4, 2, ..., 4, 1
    I = y[0] + y[-1]  # Extremos

    # Índices impares: peso 4
    I += 4 * np.sum(y[1:-1:2])

    # Índices pares (internos): peso 2
    I += 2 * np.sum(y[2:-1:2])

    I *= h / 3

    return I, x


def mostrar_resultados_simpson(f, a, b, n, I_real=None):
    """
    Muestra resultados detallados
    """
    print("="*70)
    print("REGLA DE SIMPSON 1/3 COMPUESTO")
    print("="*70 + "\n")

    try:
        I, x = simpson_1_3_compuesto(f, a, b, n)
    except ValueError as e:
        print(f"❌ Error: {e}")
        return None

    h = (b - a) / n

    print(f"Intervalo: [{a}, {b}]")
    print(f"Número de subintervalos: {n}")
    print(f"Ancho: h = {h:.6f}")

    print(f"\nAproximación de la integral:")
    print(f"  I ≈ {I:.10f}")

    if I_real is not None:
        error = abs(I - I_real)
        error_rel = error / abs(I_real) * 100
        print(f"\nValor real: {I_real:.10f}")
        print(f"Error absoluto: {error:.2e}")
        print(f"Error relativo: {error_rel:.6f}%")

    return I

