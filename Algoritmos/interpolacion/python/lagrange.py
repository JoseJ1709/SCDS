"""
Interpolación de Lagrange
Construye un polinomio que pasa por n+1 puntos dados
"""

import numpy as np
import matplotlib.pyplot as plt


def lagrange_basis(x, xi, i):
    """
    Calcula el i-ésimo polinomio base de Lagrange Li(x)

    Parámetros:
    -----------
    x : float o array
        Punto(s) donde evaluar
    xi : array
        Puntos de interpolación [x0, x1, ..., xn]
    i : int
        Índice del polinomio base

    Retorna:
    --------
    Li(x) : float o array
        Valor del polinomio base en x
    """
    n = len(xi)
    Li = np.ones_like(x, dtype=float)

    for j in range(n):
        if j != i:
            Li *= (x - xi[j]) / (xi[i] - xi[j])

    return Li


def lagrange_interpolation(xi, yi, x):
    """
    Interpolación de Lagrange

    Parámetros:
    -----------
    xi : array
        Puntos x conocidos [x0, x1, ..., xn]
    yi : array
        Valores y conocidos [y0, y1, ..., yn]
    x : float o array
        Punto(s) donde interpolar

    Retorna:
    --------
    P(x) : float o array
        Valor del polinomio interpolante en x
    """
    xi = np.array(xi)
    yi = np.array(yi)
    x = np.array(x)

    n = len(xi)
    Px = np.zeros_like(x, dtype=float)

    # P(x) = Σ yi · Li(x)
    for i in range(n):
        Li = lagrange_basis(x, xi, i)
        Px += yi[i] * Li

    return Px


def lagrange_coeficientes(xi, yi):
    """
    Calcula los coeficientes del polinomio de Lagrange
    en forma estándar: a0 + a1*x + a2*x^2 + ...

    Retorna:
    --------
    coef : array
        Coeficientes [a0, a1, a2, ..., an]
    """
    xi = np.array(xi)
    yi = np.array(yi)
    n = len(xi)

    # Usar numpy.polynomial para expandir
    coef = np.zeros(n)

    for i in range(n):
        # Construir el polinomio Li(x)
        Li_coef = np.array([yi[i]])

        for j in range(n):
            if j != i:
                # Multiplicar por (x - xj)/(xi - xj)
                factor = np.array([-xi[j], 1]) / (xi[i] - xi[j])
                Li_coef = np.convolve(Li_coef, factor)

        # Asegurar que tenga el tamaño correcto
        if len(Li_coef) < n:
            Li_coef = np.pad(Li_coef, (0, n - len(Li_coef)))

        coef += Li_coef[:n]

    return coef


def mostrar_polinomio(coef):
    """
    Muestra el polinomio en forma legible
    """
    n = len(coef)
    terminos = []

    for i, c in enumerate(coef):
        if abs(c) > 1e-10:
            if i == 0:
                terminos.append(f"{c:.6f}")
            elif i == 1:
                terminos.append(f"{c:+.6f}x")
            else:
                terminos.append(f"{c:+.6f}x^{i}")

    return " ".join(terminos)
