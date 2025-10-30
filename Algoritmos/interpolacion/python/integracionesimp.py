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


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

def ejemplo_simpson():
    """
    Ejemplos de integración con Simpson
    """
    print("\n" + "🎯"*35 + "\n")

    # Ejemplo 1: x² en [0, 1]
    print("EJEMPLO 1: ∫[0,1] x² dx = 1/3")
    print("-"*70 + "\n")

    f1 = lambda x: x**2
    a, b = 0, 1
    I_real = 1/3

    # Comparar con diferentes n
    print(f"{'n':<10} {'Aproximación':<20} {'Error':<15} {'Error Rel. (%)':<15}")
    print("-"*70)

    for n in [2, 4, 8, 16]:
        I, _ = simpson_1_3_compuesto(f1, a, b, n)
        error = abs(I - I_real)
        error_rel = error / abs(I_real) * 100
        print(f"{n:<10} {I:<20.10f} {error:<15.2e} {error_rel:<15.6f}")

    # Ejemplo 2: e^x en [0, 1]
    print("\n\n" + "="*70)
    print("EJEMPLO 2: ∫[0,1] e^x dx = e - 1")
    print("="*70 + "\n")

    f2 = lambda x: np.exp(x)
    I_real = np.e - 1

    mostrar_resultados_simpson(f2, 0, 1, n=10, I_real=I_real)

    # Comparar Trapecio vs Simpson
    comparar_metodos(f2, 0, 1, I_real)


def comparar_metodos(f, a, b, I_real):
    """
    Compara Trapecio vs Simpson
    """
    from trapecio import trapecio_compuesto

    print("\n\n" + "="*70)
    print("COMPARACIÓN: TRAPECIO vs SIMPSON 1/3")
    print("="*70 + "\n")

    print(f"{'n':<10} {'Trapecio':<20} {'Error Trap.':<15} {'Simpson':<20} {'Error Simp.':<15}")
    print("-"*90)

    for n in [2, 4, 8, 16, 32]:
        I_trap, _ = trapecio_compuesto(f, a, b, n)
        I_simp, _ = simpson_1_3_compuesto(f, a, b, n)

        error_trap = abs(I_trap - I_real)
        error_simp = abs(I_simp - I_real)

        print(f"{n:<10} {I_trap:<20.10f} {error_trap:<15.2e} {I_simp:<20.10f} {error_simp:<15.2e}")

    # Graficar convergencia
    graficar_comparacion(f, a, b, I_real)


def graficar_comparacion(f, a, b, I_real):
    """
    Gráfica de convergencia: Trapecio vs Simpson
    """
    from trapecio import trapecio_compuesto

    ns = np.array([2, 4, 8, 16, 32, 64, 128])
    errores_trap = []
    errores_simp = []

    for n in ns:
        I_trap, _ = trapecio_compuesto(f, a, b, n)
        I_simp, _ = simpson_1_3_compuesto(f, a, b, n)

        errores_trap.append(abs(I_trap - I_real))
        errores_simp.append(abs(I_simp - I_real))

    plt.figure(figsize=(10, 6))
    plt.loglog(ns, errores_trap, 'ro-', linewidth=2, markersize=8, label='Trapecio')
    plt.loglog(ns, errores_simp, 'bs-', linewidth=2, markersize=8, label='Simpson 1/3')

    plt.grid(True, alpha=0.3)
    plt.xlabel('Número de subintervalos (n)', fontsize=12)
    plt.ylabel('Error absoluto', fontsize=12)
    plt.title('Convergencia: Trapecio vs Simpson', fontsize=14, fontweight='bold')
    plt.legend(fontsize=12)

    plt.tight_layout()
    plt.savefig('comparacion_integracion.png', dpi=300)
    print(f"\n✅ Gráfica guardada como 'comparacion_integracion.png'")
    plt.show()


if __name__ == "__main__":
    ejemplo_simpson()