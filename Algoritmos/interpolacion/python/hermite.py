"""
Interpolación de Hermite
Interpola valores Y derivadas de la función
"""

import numpy as np
import matplotlib.pyplot as plt


def hermite_diferencias_divididas(xi, yi, dyi):
    """
    Calcula la tabla de diferencias divididas para Hermite

    Parámetros:
    -----------
    xi : array
        Puntos x conocidos
    yi : array
        Valores y conocidos
    dyi : array
        Derivadas dy/dx conocidas

    Retorna:
    --------
    z : array
        Puntos z (xi duplicados)
    tabla : matriz
        Tabla de diferencias divididas
    """
    xi = np.array(xi, dtype=float)
    yi = np.array(yi, dtype=float)
    dyi = np.array(dyi, dtype=float)
    n = len(xi)

    # Crear array z con puntos duplicados
    z = np.zeros(2 * n)
    z[0::2] = xi  # Índices pares
    z[1::2] = xi  # Índices impares

    # Tabla de diferencias divididas
    m = 2 * n
    tabla = np.zeros((m, m))

    # Primera columna: valores f(xi)
    tabla[0::2, 0] = yi
    tabla[1::2, 0] = yi

    # Segunda columna: derivadas f'(xi)
    tabla[0::2, 1] = dyi

    # Para puntos duplicados: f[zi, zi+1] ya está en la derivada
    for i in range(1, m - 1, 2):
        tabla[i, 1] = (tabla[i + 1, 0] - tabla[i, 0]) / (z[i + 1] - z[i])

    # Resto de la tabla
    for j in range(2, m):
        for i in range(m - j):
            tabla[i, j] = (tabla[i + 1, j - 1] - tabla[i, j - 1]) / (z[i + j] - z[i])

    return z, tabla


def hermite_interpolation(xi, yi, dyi, x, z=None, tabla=None):
    """
    Interpolación de Hermite

    Parámetros:
    -----------
    xi : array
        Puntos x conocidos
    yi : array
        Valores y conocidos
    dyi : array
        Derivadas conocidas
    x : float o array
        Punto(s) donde interpolar
    z, tabla : arrays opcionales
        Precalculados

    Retorna:
    --------
    P(x) : float o array
        Valor del polinomio
    """
    x = np.array(x, dtype=float)

    # Calcular tabla si no se proporciona
    if z is None or tabla is None:
        z, tabla = hermite_diferencias_divididas(xi, yi, dyi)

    m = len(z)

    # Evaluar polinomio de Newton con puntos z
    Px = tabla[0, 0] * np.ones_like(x, dtype=float)
    producto = np.ones_like(x, dtype=float)

    for i in range(1, m):
        producto *= (x - z[i - 1])
        Px += tabla[0, i] * producto

    return Px


def mostrar_tabla_hermite(xi, yi, dyi, z, tabla):
    """
    Muestra la tabla de diferencias divididas de Hermite
    """
    n = len(xi)
    m = 2 * n

    print("\nTabla de Diferencias Divididas de Hermite:")
    print("=" * 100)
    print(f"{'i':<5} {'z[i]':<10} {'f[z[i]]':<15} {'f[z[i],z[i+1]]':<20} {'f[z[i],z[i+1],z[i+2]]':<25} {'...'}")
    print("-" * 100)

    for i in range(m):
        row = f"{i:<5} {z[i]:<10.4f} {tabla[i, 0]:<15.6f} "
        if i < m - 1:
            row += f"{tabla[i, 1]:<20.6f} "
        else:
            row += f"{'':20} "
        if i < m - 2:
            row += f"{tabla[i, 2]:<25.6f}"
        print(row)

    print("=" * 100)

    print(f"\nPuntos originales: {n}")
    print(f"Puntos en tabla z (duplicados): {m}")
    print(f"Grado del polinomio: {m - 1}")
