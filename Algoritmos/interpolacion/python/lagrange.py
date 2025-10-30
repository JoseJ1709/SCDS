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


# ============================================================================
# EJEMPLO DE USO Y VISUALIZACIÓN
# ============================================================================

def ejemplo_lagrange():
    """
    Ejemplo completo de interpolación de Lagrange
    """
    print("=" * 70)
    print("INTERPOLACIÓN DE LAGRANGE")
    print("=" * 70 + "\n")

    # Datos de ejemplo
    xi = np.array([0, 1, 2, 3])
    yi = np.array([1, 3, 2, 5])

    print("Puntos dados:")
    print(f"x = {xi}")
    print(f"y = {yi}\n")

    # Calcular coeficientes
    coef = lagrange_coeficientes(xi, yi)
    print("Polinomio interpolante:")
    print(f"P(x) = {mostrar_polinomio(coef)}\n")

    # Evaluar en puntos específicos
    x_test = np.array([0.5, 1.5, 2.5])
    y_test = lagrange_interpolation(xi, yi, x_test)

    print("Evaluación en puntos intermedios:")
    for x, y in zip(x_test, y_test):
        print(f"  P({x}) = {y:.6f}")

    # Verificar que pasa por los puntos originales
    print("\nVerificación (debe dar los valores originales):")
    y_verif = lagrange_interpolation(xi, yi, xi)
    for x, y_orig, y_calc in zip(xi, yi, y_verif):
        print(f"  P({x}) = {y_calc:.6f}  (original: {y_orig})")

    # Graficar
    graficar_interpolacion(xi, yi, lagrange_interpolation,
                           titulo="Interpolación de Lagrange")


def graficar_interpolacion(xi, yi, metodo, titulo="Interpolación"):
    """
    Grafica los puntos y el polinomio interpolante
    """
    # Generar puntos para la curva
    x_plot = np.linspace(min(xi) - 0.5, max(xi) + 0.5, 500)
    y_plot = metodo(xi, yi, x_plot)

    # Crear gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='Polinomio interpolante')
    plt.plot(xi, yi, 'ro', markersize=10, label='Puntos dados')

    # Marcar los puntos con coordenadas
    for x, y in zip(xi, yi):
        plt.annotate(f'({x}, {y})', (x, y),
                     xytext=(5, 5), textcoords='offset points')

    plt.grid(True, alpha=0.3)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{titulo.lower().replace(" ", "_")}.png', dpi=300)
    print(f"\n✅ Gráfica guardada como '{titulo.lower().replace(' ', '_')}.png'")
    plt.show()


if __name__ == "__main__":
    ejemplo_lagrange()

    # Ejemplo adicional: función conocida
    print("\n\n" + "=" * 70)
    print("EJEMPLO 2: Interpolando sen(x)")
    print("=" * 70 + "\n")

    xi = np.array([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])
    yi = np.sin(xi)

    print(f"Puntos: x = {xi}")
    print(f"        y = {yi}\n")

    # Evaluar en puntos intermedios
    x_test = np.pi / 3
    y_interp = lagrange_interpolation(xi, yi, x_test)
    y_real = np.sin(x_test)

    print(f"Interpolación en x = π/3:")
    print(f"  Valor interpolado: {y_interp:.6f}")
    print(f"  Valor real sen(π/3): {y_real:.6f}")
    print(f"  Error: {abs(y_interp - y_real):.6f}")

    graficar_interpolacion(xi, yi, lagrange_interpolation,
                           titulo="Interpolación de sen(x) con Lagrange")