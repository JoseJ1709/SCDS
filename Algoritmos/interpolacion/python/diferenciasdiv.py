"""
Interpolación por Diferencias Divididas (Método de Newton)
Más eficiente que Lagrange para agregar nuevos puntos
"""

import numpy as np
import matplotlib.pyplot as plt


def diferencias_divididas(xi, yi):
    """
    Calcula la tabla de diferencias divididas

    Parámetros:
    -----------
    xi : array
        Puntos x conocidos
    yi : array
        Valores y conocidos

    Retorna:
    --------
    tabla : matriz
        Tabla de diferencias divididas completa
    """
    xi = np.array(xi, dtype=float)
    yi = np.array(yi, dtype=float)
    n = len(xi)

    # Crear tabla (matriz triangular superior)
    tabla = np.zeros((n, n))
    tabla[:, 0] = yi  # Primera columna = valores yi

    # Calcular diferencias divididas
    for j in range(1, n):
        for i in range(n - j):
            tabla[i, j] = (tabla[i + 1, j - 1] - tabla[i, j - 1]) / (xi[i + j] - xi[i])

    return tabla


def newton_interpolation(xi, yi, x, tabla=None):
    """
    Interpolación usando diferencias divididas

    Parámetros:
    -----------
    xi : array
        Puntos x conocidos
    yi : array
        Valores y conocidos
    x : float o array
        Punto(s) donde interpolar
    tabla : matriz (opcional)
        Tabla de diferencias divididas precalculada

    Retorna:
    --------
    P(x) : float o array
        Valor del polinomio en x
    """
    xi = np.array(xi, dtype=float)
    yi = np.array(yi, dtype=float)
    x = np.array(x, dtype=float)

    # Calcular tabla si no se proporciona
    if tabla is None:
        tabla = diferencias_divididas(xi, yi)

    n = len(xi)

    # P(x) = f[x0] + f[x0,x1](x-x0) + f[x0,x1,x2](x-x0)(x-x1) + ...
    Px = tabla[0, 0] * np.ones_like(x, dtype=float)
    producto = np.ones_like(x, dtype=float)

    for i in range(1, n):
        producto *= (x - xi[i - 1])
        Px += tabla[0, i] * producto

    return Px


def mostrar_tabla_diferencias(xi, yi, tabla):
    """
    Muestra la tabla de diferencias divididas de forma legible
    """
    n = len(xi)

    print("\nTabla de Diferencias Divididas:")
    print("=" * 80)

    # Encabezado
    header = f"{'i':<5} {'xi':<10} {'f[xi]':<15}"
    for j in range(1, n):
        if j == 1:
            header += f"{'f[xi,xi+1]':<15}"
        elif j == 2:
            header += f"{'f[xi,xi+1,xi+2]':<18}"
        else:
            header += f"{'f[...]':<18}"
    print(header)
    print("-" * 80)

    # Datos
    for i in range(n):
        row = f"{i:<5} {xi[i]:<10.4f} "
        for j in range(n):
            if j <= n - i - 1:
                if tabla[i, j] != 0 or j == 0:
                    if j == 0:
                        row += f"{tabla[i, j]:<15.6f}"
                    elif j == 1:
                        row += f"{tabla[i, j]:<15.6f}"
                    else:
                        row += f"{tabla[i, j]:<18.6f}"
        print(row)

    print("=" * 80)

    # Coeficientes del polinomio
    print(f"\nCoeficientes del polinomio de Newton:")
    print(f"a0 = {tabla[0, 0]:.6f}")
    for i in range(1, n):
        print(f"a{i} = {tabla[0, i]:.6f}")


def construir_polinomio_newton(xi, tabla):
    """
    Construye la representación simbólica del polinomio de Newton
    """
    n = len(xi)
    terminos = [f"{tabla[0, 0]:.6f}"]

    for i in range(1, n):
        # Construir el producto (x - x0)(x - x1)...(x - xi-1)
        factores = []
        for j in range(i):
            if xi[j] >= 0:
                factores.append(f"(x - {xi[j]:.2f})")
            else:
                factores.append(f"(x + {-xi[j]:.2f})")

        producto = "".join(factores)
        terminos.append(f"{tabla[0, i]:+.6f}·{producto}")

    return "P(x) = " + " ".join(terminos)


