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


def explicacion_romberg():
    """
    Explicación paso a paso del método de Romberg
    """
    print("\n" + "📚" * 40)
    print("EXPLICACIÓN DEL MÉTODO DE ROMBERG")
    print("📚" * 40 + "\n")

    print("""
╔════════════════════════════════════════════════════════════════════╗
║  ¿CÓMO FUNCIONA ROMBERG?                                           ║
╚════════════════════════════════════════════════════════════════════╝

1️⃣  PASO 1: Calcular primera columna (Trapecios)
   ────────────────────────────────────────────────────
   R(0,0) = Trapecio con 1 subintervalo (h = b-a)
   R(1,0) = Trapecio con 2 subintervalos (h = (b-a)/2)
   R(2,0) = Trapecio con 4 subintervalos (h = (b-a)/4)
   R(3,0) = Trapecio con 8 subintervalos (h = (b-a)/8)
   ...

2️⃣  PASO 2: Extrapolación de Richardson
   ────────────────────────────────────────────────────
   Combina valores previos para eliminar términos de error

   Fórmula: R(i,j) = R(i,j-1) + [R(i,j-1) - R(i-1,j-1)]
                                 ──────────────────────
                                       4^j - 1

3️⃣  RESULTADO: Diagonal principal
   ────────────────────────────────────────────────────
   R(0,0) → error O(h²)
   R(1,1) → error O(h⁴)  ← ¡2 órdenes mejor!
   R(2,2) → error O(h⁶)  ← ¡4 órdenes mejor!
   R(3,3) → error O(h⁸)  ← ¡6 órdenes mejor!

╔════════════════════════════════════════════════════════════════════╗
║  🎯 VENTAJA CLAVE: Precisión exponencial con poco esfuerzo        ║
╚════════════════════════════════════════════════════════════════════╝
""")


# ============================================================================
# EJEMPLO DETALLADO PASO A PASO
# ============================================================================

def ejemplo_romberg_paso_a_paso():
    """
    Ejemplo completamente detallado del método de Romberg
    """
    print("\n" + "🔍" * 40)
    print("EJEMPLO PASO A PASO: ∫[0,1] x² dx = 1/3")
    print("🔍" * 40 + "\n")

    f = lambda x: x ** 2
    a, b = 0, 1
    I_real = 1 / 3

    # Nivel 0: Trapecio simple
    print("━" * 80)
    print("NIVEL 0: Trapecio con n=1 (h = 1)")
    print("━" * 80)
    h0 = b - a
    R_0_0 = h0 * (f(a) + f(b)) / 2
    print(f"R(0,0) = {h0} * [{f(a)} + {f(b)}] / 2")
    print(f"R(0,0) = {R_0_0:.12f}")
    print(f"Error: {abs(R_0_0 - I_real):.2e}\n")

    # Nivel 1: h = 0.5
    print("━" * 80)
    print("NIVEL 1: Trapecio con n=2 (h = 0.5)")
    print("━" * 80)
    h1 = h0 / 2
    x_medio = a + h1
    print(f"Punto nuevo: x = {x_medio}")
    print(f"f({x_medio}) = {f(x_medio)}")

    R_1_0 = R_0_0 / 2 + h1 * f(x_medio)
    print(f"\nR(1,0) = R(0,0)/2 + h * f({x_medio})")
    print(f"R(1,0) = {R_0_0}/2 + {h1} * {f(x_medio)}")
    print(f"R(1,0) = {R_1_0:.12f}")
    print(f"Error: {abs(R_1_0 - I_real):.2e}")

    # Extrapolación
    print(f"\n🔄 EXTRAPOLACIÓN:")
    R_1_1 = R_1_0 + (R_1_0 - R_0_0) / (4 ** 1 - 1)
    print(f"R(1,1) = R(1,0) + [R(1,0) - R(0,0)] / (4¹ - 1)")
    print(f"R(1,1) = {R_1_0:.12f} + [{R_1_0:.12f} - {R_0_0:.12f}] / 3")
    print(f"R(1,1) = {R_1_1:.12f}")
    print(f"Error: {abs(R_1_1 - I_real):.2e}")
    print(f"✨ ¡Mejora de {abs(R_1_0 - I_real) / abs(R_1_1 - I_real):.1f}x!\n")

    # Nivel 2
    print("━" * 80)
    print("NIVEL 2: Trapecio con n=4 (h = 0.25)")
    print("━" * 80)
    h2 = h1 / 2
    puntos_nuevos = [a + h2, a + 3 * h2]
    suma = sum(f(x) for x in puntos_nuevos)

    print(f"Puntos nuevos: {puntos_nuevos}")
    print(f"Suma: {suma}")

    R_2_0 = R_1_0 / 2 + h2 * suma
    print(f"\nR(2,0) = {R_2_0:.12f}")

    R_2_1 = R_2_0 + (R_2_0 - R_1_0) / 3
    print(f"R(2,1) = {R_2_1:.12f}")

    R_2_2 = R_2_1 + (R_2_1 - R_1_1) / 15
    print(f"R(2,2) = {R_2_2:.12f}")
    print(f"Error: {abs(R_2_2 - I_real):.2e}")
    print(f"✨ ¡Casi perfecto!\n")


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

def ejemplo_romberg_completo():
    """
    Ejemplos completos de Romberg
    """
    explicacion_romberg()
    ejemplo_romberg_paso_a_paso()

    # Ejemplo 1: x² en [0,1]
    print("\n\n" + "═" * 80)
    print("EJEMPLO 1: ∫[0,1] x² dx = 1/3")
    print("═" * 80 + "\n")

    f1 = lambda x: x ** 2
    I_real1 = 1 / 3

    I1, R1 = romberg(f1, 0, 1, n_max=6, tol=1e-10)

    print(f"\n✅ RESULTADO FINAL: {I1:.15f}")
    print(f"   Valor real:      {I_real1:.15f}")
    print(f"   Error absoluto:  {abs(I1 - I_real1):.2e}")

    # Ejemplo 2: sin(x) en [0, π]
    print("\n\n" + "═" * 80)
    print("EJEMPLO 2: ∫[0,π] sin(x) dx = 2")
    print("═" * 80 + "\n")

    f2 = lambda x: np.sin(x)
    I_real2 = 2.0

    I2, R2 = romberg(f2, 0, np.pi, n_max=8, tol=1e-12)

    print(f"\n✅ RESULTADO FINAL: {I2:.15f}")
    print(f"   Valor real:      {I_real2:.15f}")
    print(f"   Error absoluto:  {abs(I2 - I_real2):.2e}")

    # Comparar con otros métodos
    comparar_metodos_integracion(f2, 0, np.pi, I_real2)


def comparar_metodos_integracion(f, a, b, I_real):
    """
    Compara Trapecio, Simpson y Romberg
    """
    from trapecio import trapecio_compuesto
    from simpson import simpson_1_3_compuesto

    print("\n\n" + "═" * 80)
    print("COMPARACIÓN: TRAPECIO vs SIMPSON vs ROMBERG")
    print("═" * 80 + "\n")

    print(f"{'Método':<20} {'n/nivel':<10} {'Resultado':<20} {'Error':<15} {'Evaluaciones':<15}")
    print("─" * 80)

    # Trapecio con n=64
    I_trap, _ = trapecio_compuesto(f, a, b, 64)
    error_trap = abs(I_trap - I_real)
    print(f"{'Trapecio':<20} {64:<10} {I_trap:<20.12f} {error_trap:<15.2e} {65:<15}")

    # Simpson con n=64
    I_simp, _ = simpson_1_3_compuesto(f, a, b, 64)
    error_simp = abs(I_simp - I_real)
    print(f"{'Simpson 1/3':<20} {64:<10} {I_simp:<20.12f} {error_simp:<15.2e} {65:<15}")

    # Romberg nivel 6 (equivale a n=64)
    I_romb, _ = romberg(f, a, b, n_max=7, tol=1e-15, mostrar_tabla=False)
    error_romb = abs(I_romb - I_real)
    evals_romb = 1 + 2 + 4 + 8 + 16 + 32 + 64  # Evaluaciones acumuladas
    print(f"{'Romberg':<20} {6:<10} {I_romb:<20.12f} {error_romb:<15.2e} {evals_romb:<15}")

    print("\n💡 Observación:")
    print(f"   Romberg es {error_trap / error_romb:.0f}x más preciso que Trapecio")
    print(f"   Romberg es {error_simp / error_romb:.0f}x más preciso que Simpson")

    # Graficar convergencia
    graficar_convergencia_romberg(f, a, b, I_real)


def graficar_convergencia_romberg(f, a, b, I_real):
    """
    Grafica la convergencia de Romberg
    """
    # Calcular Romberg hasta nivel 10
    _, R = romberg(f, a, b, n_max=10, tol=0, mostrar_tabla=False)

    niveles = range(R.shape[0])
    errores_diagonal = [abs(R[i, i] - I_real) if R[i, i] != 0 else np.nan
                        for i in niveles]

    # Filtrar valores válidos
    niveles_validos = [i for i, e in enumerate(errores_diagonal) if not np.isnan(e) and e > 0]
    errores_validos = [errores_diagonal[i] for i in niveles_validos]

    plt.figure(figsize=(10, 6))
    plt.semilogy(niveles_validos, errores_validos, 'bo-', linewidth=2, markersize=8)
    plt.grid(True, alpha=0.3)
    plt.xlabel('Nivel de Romberg', fontsize=12)
    plt.ylabel('Error absoluto', fontsize=12)
    plt.title('Convergencia del Método de Romberg', fontsize=14, fontweight='bold')

    # Añadir anotaciones
    for i, (nivel, error) in enumerate(zip(niveles_validos[:5], errores_validos[:5])):
        plt.annotate(f'{error:.2e}', (nivel, error),
                     textcoords="offset points", xytext=(0, 10), ha='center')

    plt.tight_layout()
    plt.savefig('romberg_convergencia.png', dpi=300)
    print(f"\n✅ Gráfica guardada como 'romberg_convergencia.png'")
    plt.show()


if __name__ == "__main__":
    ejemplo_romberg_completo()