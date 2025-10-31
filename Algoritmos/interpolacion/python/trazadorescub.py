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


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

def ejemplo_trazadores_naturales():
    """
    Ejemplo de trazadores cúbicos naturales
    """
    print("=" * 80)
    print("TRAZADORES CÚBICOS NATURALES")
    print("=" * 80 + "\n")

    # Datos de ejemplo
    xi = np.array([0, 1, 2, 3, 4])
    yi = np.array([0, 0.5, 2.0, 1.5, 1.0])

    print("Puntos dados:")
    for x, y in zip(xi, yi):
        print(f"  ({x}, {y})")

    # Calcular trazadores_cubicos
    coef = trazadores_cubicos_naturales(xi, yi)
    mostrar_coeficientes_trazadores_cubicos(xi, coef)

    # Evaluar en puntos
    x_test = np.array([0.5, 1.5, 2.5, 3.5])
    print("\nEvaluación en puntos intermedios:")
    for x in x_test:
        y = evaluar_trazadores_cubicos(xi, coef, x)
        dy = derivada_trazadores_cubicos(xi, coef, x)
        ddy = segunda_derivada_trazadores_cubicos(xi, coef, x)
        print(f"  x={x:.1f}: S(x)={y:.6f}, S'(x)={dy:.6f}, S''(x)={ddy:.6f}")

    # Verificar condiciones naturales
    print(f"\nVerificación de condiciones naturales:")
    print(f"  S''({xi[0]}) = {segunda_derivada_trazadores_cubicos(xi, coef, xi[0]):.6f} (debe ser ≈0)")
    print(f"  S''({xi[-1]}) = {segunda_derivada_trazadores_cubicos(xi, coef, xi[-1]):.6f} (debe ser ≈0)")

    # Graficar
    graficar_trazadores_cubicos(xi, yi, coef, titulo="Trazadores Cúbicos Naturales")


def ejemplo_trazadores_sujetos():
    """
    Ejemplo de trazadores cúbicos sujetos (con derivadas en extremos)
    """
    print("\n\n" + "=" * 80)
    print("TRAZADORES CÚBICOS SUJETOS")
    print("=" * 80 + "\n")

    # Datos de ejemplo
    xi = np.array([0, 1, 2, 3])
    yi = np.array([0, 1, 0, 1])
    dy0 = 0.5  # Pendiente en x=0
    dyn = -0.5  # Pendiente en x=3

    print("Puntos dados:")
    for x, y in zip(xi, yi):
        print(f"  ({x}, {y})")
    print(f"\nCondiciones en extremos:")
    print(f"  S'({xi[0]}) = {dy0}")
    print(f"  S'({xi[-1]}) = {dyn}")

    # Calcular trazadores_cubicos
    coef = trazadores_cubicos_sujetos(xi, yi, dy0, dyn)
    mostrar_coeficientes_trazadores_cubicos(xi, coef)

    # Verificar condiciones
    print(f"\nVerificación:")
    print(f"  S'({xi[0]}) = {derivada_trazadores_cubicos(xi, coef, xi[0]):.6f} (debe ser {dy0})")
    print(f"  S'({xi[-1]}) = {derivada_trazadores_cubicos(xi, coef, xi[-1]):.6f} (debe ser {dyn})")

    # Graficar
    graficar_trazadores_cubicos(xi, yi, coef, titulo="Trazadores Cúbicos Sujetos")


def graficar_trazadores_cubicos(xi, yi, coeficientes, titulo="Trazadores Cúbicos"):
    """
    Grafica el trazadores_cubicos con sus derivadas
    """
    # Puntos para graficar
    x_plot = np.linspace(xi[0], xi[-1], 500)
    y_plot = evaluar_trazadores_cubicos(xi, coeficientes, x_plot)
    dy_plot = derivada_trazadores_cubicos(xi, coeficientes, x_plot)
    ddy_plot = segunda_derivada_trazadores_cubicos(xi, coeficientes, x_plot)

    # Crear figura con 3 subgráficas
    fig, axes = plt.subplots(3, 1, figsize=(10, 10))

    # S(x)
    axes[0].plot(x_plot, y_plot, 'b-', linewidth=2, label='S(x)')
    axes[0].plot(xi, yi, 'ro', markersize=10, label='Puntos dados')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylabel('S(x)', fontsize=12)
    axes[0].set_title(titulo, fontsize=14, fontweight='bold')
    axes[0].legend()

    # S'(x)
    axes[1].plot(x_plot, dy_plot, 'g-', linewidth=2, label="S'(x)")
    axes[1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylabel("S'(x)", fontsize=12)
    axes[1].legend()

    # S''(x)
    axes[2].plot(x_plot, ddy_plot, 'r-', linewidth=2, label="S''(x)")
    axes[2].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[2].grid(True, alpha=0.3)
    axes[2].set_xlabel('x', fontsize=12)
    axes[2].set_ylabel("S''(x)", fontsize=12)
    axes[2].legend()

    plt.tight_layout()
    filename = titulo.lower().replace(" ", "_") + ".png"
    plt.savefig(filename, dpi=300)
    print(f"\n✅ Gráfica guardada como '{filename}'")
    plt.show()


def comparar_con_polinomio():
    """
    Compara trazadores_cubicos vs polinomio de interpolación
    """
    print("\n\n" + "=" * 80)
    print("COMPARACIÓN: trazadores_cubicos vs POLINOMIO DE LAGRANGE")
    print("=" * 80 + "\n")

    from lagrange import lagrange_interpolation

    # Función de Runge (problemática para interpolación polinomial)
    xi = np.linspace(-5, 5, 9)
    yi = 1 / (1 + xi ** 2)

    print("Interpolando la función de Runge: f(x) = 1/(1+x²)")
    print(f"Con {len(xi)} puntos en [-5, 5]\n")

    # Calcular ambos
    coef_trazadores_cubicos = trazadores_cubicos_naturales(xi, yi)

    # Graficar comparación
    x_plot = np.linspace(-5, 5, 500)
    y_real = 1 / (1 + x_plot ** 2)
    y_trazadores_cubicos = evaluar_trazadores_cubicos(xi, coef_trazadores_cubicos, x_plot)
    y_lagrange = lagrange_interpolation(xi, yi, x_plot)

    plt.figure(figsize=(12, 6))
    plt.plot(x_plot, y_real, 'k-', linewidth=2, label='Función real', alpha=0.7)
    plt.plot(x_plot, y_trazadores_cubicos, 'b-', linewidth=2, label='trazadores_cubicos cúbico')
    plt.plot(x_plot, y_lagrange, 'r--', linewidth=2, label='Lagrange')
    plt.plot(xi, yi, 'go', markersize=8, label='Puntos dados')
    plt.grid(True, alpha=0.3)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('trazadores_cubicos vs Lagrange: Función de Runge', fontsize=14, fontweight='bold')
    plt.legend()
    plt.ylim(-0.5, 1.5)
    plt.tight_layout()
    plt.savefig('comparacion_trazadores_cubicos_lagrange.png', dpi=300)
    print("✅ Gráfica guardada como 'comparacion_trazadores_cubicos_lagrange.png'")
    plt.show()

    # Calcular errores
    error_trazadores_cubicos = np.mean(np.abs(y_trazadores_cubicos - y_real))
    error_lagrange = np.mean(np.abs(y_lagrange - y_real))

    print(f"\nError promedio:")
    print(f"  trazadores_cubicos:   {error_trazadores_cubicos:.6f}")
    print(f"  Lagrange: {error_lagrange:.6f}")
    print(f"\n🏆 trazadores_cubicos es {error_lagrange / error_trazadores_cubicos:.2f}x mejor!")


if __name__ == "__main__":
    ejemplo_trazadores_naturales()
    ejemplo_trazadores_sujetos()
    comparar_con_polinomio()