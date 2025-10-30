"""
Interpolación Cúbica Fija
Para exactamente 4 puntos (polinomio cúbico único)
P(x) = a0 + a1*x + a2*x^2 + a3*x^3
"""

import numpy as np
import matplotlib.pyplot as plt


def interpolacion_cubica_fija(xi, yi):
    """
    Interpolación con polinomio cúbico para 4 puntos

    Parámetros:
    -----------
    xi : array de 4 elementos
        Puntos x
    yi : array de 4 elementos
        Valores y

    Retorna:
    --------
    coef : array [a0, a1, a2, a3]
        Coeficientes del polinomio cúbico
    """
    if len(xi) != 4 or len(yi) != 4:
        raise ValueError("Se requieren exactamente 4 puntos")

    xi = np.array(xi, dtype=float)
    yi = np.array(yi, dtype=float)

    # Sistema: V * a = y
    # donde V es la matriz de Vandermonde
    V = np.column_stack([np.ones(4), xi, xi ** 2, xi ** 3])

    # Resolver sistema
    coef = np.linalg.solve(V, yi)

    return coef


def evaluar_cubica(coef, x):
    """
    Evalúa el polinomio cúbico en x
    P(x) = a0 + a1*x + a2*x^2 + a3*x^3
    """
    x = np.array(x)
    a0, a1, a2, a3 = coef
    return a0 + a1 * x + a2 * x ** 2 + a3 * x ** 3


def derivada_cubica(coef, x):
    """
    Derivada del polinomio cúbico
    P'(x) = a1 + 2*a2*x + 3*a3*x^2
    """
    x = np.array(x)
    a0, a1, a2, a3 = coef
    return a1 + 2 * a2 * x + 3 * a3 * x ** 2


def segunda_derivada_cubica(coef, x):
    """
    Segunda derivada del polinomio cúbico
    P''(x) = 2*a2 + 6*a3*x
    """
    x = np.array(x)
    a0, a1, a2, a3 = coef
    return 2 * a2 + 6 * a3 * x


def mostrar_polinomio_cubico(coef):
    """
    Muestra el polinomio en forma legible
    """
    a0, a1, a2, a3 = coef
    print(f"\nPolinomio cúbico:")
    print(f"P(x) = {a0:.6f} {a1:+.6f}x {a2:+.6f}x² {a3:+.6f}x³")


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

def ejemplo_cubica_fija():
    """
    Ejemplo de interpolación cúbica con 4 puntos
    """
    print("=" * 70)
    print("INTERPOLACIÓN CÚBICA FIJA (4 PUNTOS)")
    print("=" * 70 + "\n")

    # Exactamente 4 puntos
    xi = np.array([0, 1, 2, 3])
    yi = np.array([1, 2, 0, 4])

    print("Puntos dados:")
    for x, y in zip(xi, yi):
        print(f"  ({x}, {y})")

    # Calcular coeficientes
    coef = interpolacion_cubica_fija(xi, yi)
    mostrar_polinomio_cubico(coef)

    # Verificar que pasa por los puntos
    print("\nVerificación:")
    for x, y in zip(xi, yi):
        p_x = evaluar_cubica(coef, x)
        print(f"  P({x}) = {p_x:.6f} (debe ser {y})")

    # Evaluar en punto intermedio
    x_test = 1.5
    y_test = evaluar_cubica(coef, x_test)
    dy_test = derivada_cubica(coef, x_test)
    ddy_test = segunda_derivada_cubica(coef, x_test)

    print(f"\nEvaluación en x = {x_test}:")
    print(f"  P({x_test}) = {y_test:.6f}")
    print(f"  P'({x_test}) = {dy_test:.6f}")
    print(f"  P''({x_test}) = {ddy_test:.6f}")

    # Graficar
    x_plot = np.linspace(min(xi) - 0.5, max(xi) + 0.5, 500)
    y_plot = evaluar_cubica(coef, x_plot)

    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='Polinomio cúbico')
    plt.plot(xi, yi, 'ro', markersize=10, label='Puntos dados')

    for x, y in zip(xi, yi):
        plt.annotate(f'({x}, {y})', (x, y),
                     xytext=(5, 5), textcoords='offset points')

    plt.grid(True, alpha=0.3)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Interpolación Cúbica (4 puntos)', fontsize=14, fontweight='bold')
    plt.legend()
    plt.tight_layout()
    plt.savefig('interpolacion_cubica_fija.png', dpi=300)
    print("\n✅ Gráfica guardada como 'interpolacion_cubica_fija.png'")
    plt.show()


def comparar_metodos_cubicos():
    """
    Compara interpolación cúbica fija vs spline cúbico
    """
    print("\n\n" + "=" * 70)
    print("COMPARACIÓN: CÚBICA FIJA vs SPLINE CÚBICO")
    print("=" * 70 + "\n")

    from trazadores_cubicos import trazadores_cubicos_naturales, evaluar_spline

    # 5 puntos
    xi = np.array([0, 1, 2, 3, 4])
    yi = np.array([0, 1, 0, 1, 0])

    # Spline cúbico (usa todos los puntos)
    coef_spline = trazadores_cubicos_naturales(xi, yi)

    # Cúbica fija (solo primeros 4 puntos)
    xi_cubica = xi[:4]
    yi_cubica = yi[:4]
    coef_cubica = interpolacion_cubica_fija(xi_cubica, yi_cubica)

    # Graficar
    x_plot = np.linspace(0, 4, 500)
    y_spline = evaluar_spline(xi, coef_spline, x_plot)
    y_cubica = evaluar_cubica(coef_cubica, x_plot)

    plt.figure(figsize=(12, 6))
    plt.plot(x_plot, y_spline, 'b-', linewidth=2, label='Spline cúbico (5 puntos)')
    plt.plot(x_plot, y_cubica, 'r--', linewidth=2, label='Cúbica fija (4 puntos)')
    plt.plot(xi, yi, 'go', markersize=10, label='Todos los puntos')
    plt.plot(xi_cubica, yi_cubica, 'ro', markersize=8, label='Puntos usados (cúbica)')
    plt.grid(True, alpha=0.3)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Spline vs Cúbica Fija', fontsize=14, fontweight='bold')
    plt.legend()
    plt.tight_layout()
    plt.savefig('comparacion_cubica_spline.png', dpi=300)
    print("✅ Gráfica guardada")
    plt.show()

    print("\n💡 Nota:")
    print("  - Cúbica fija: UN polinomio de grado 3 para 4 puntos")
    print("  - Spline: MÚLTIPLES polinomios de grado 3, uno por segmento")
    print("  - Spline es más flexible y no oscila")


if __name__ == "__main__":
    ejemplo_cubica_fija()
    comparar_metodos_cubicos()