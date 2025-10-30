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


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

def ejemplo_hermite():
    """
    Ejemplo completo de interpolación de Hermite
    """
    print("=" * 80)
    print("INTERPOLACIÓN DE HERMITE")
    print("=" * 80 + "\n")

    # Datos de ejemplo
    xi = np.array([1.3, 1.6, 1.9])
    yi = np.array([0.6200860, 0.4554022, 0.2818186])
    dyi = np.array([-0.5220232, -0.5698959, -0.5811571])  # Derivadas

    print("Datos dados:")
    print(f"{'x':<10} {'y = f(x)':<15} {'y\' = f\'(x)':<15}")
    print("-" * 40)
    for x, y, dy in zip(xi, yi, dyi):
        print(f"{x:<10.1f} {y:<15.7f} {dy:<15.7f}")

    # Calcular tabla
    z, tabla = hermite_diferencias_divididas(xi, yi, dyi)
    mostrar_tabla_hermite(xi, yi, dyi, z, tabla)

    # Evaluar en un punto
    x_test = 1.5
    y_interp = hermite_interpolation(xi, yi, dyi, x_test, z, tabla)
    print(f"\nInterpolación en x = {x_test}:")
    print(f"  P({x_test}) = {y_interp:.7f}")

    # Comparar con interpolación simple (sin derivadas)
    from diferencias_divididas import newton_interpolation
    y_newton = newton_interpolation(xi, yi, x_test)
    print(f"  Newton simple: {y_newton:.7f}")
    print(f"  Diferencia: {abs(y_interp - y_newton):.7f}")

    # Graficar
    x_plot = np.linspace(min(xi) - 0.2, max(xi) + 0.2, 500)
    y_hermite = hermite_interpolation(xi, yi, dyi, x_plot, z, tabla)
    y_newton_plot = newton_interpolation(xi, yi, x_plot)

    plt.figure(figsize=(12, 6))
    plt.plot(x_plot, y_hermite, 'b-', linewidth=2, label='Hermite (con derivadas)')
    plt.plot(x_plot, y_newton_plot, 'g--', linewidth=2, label='Newton (sin derivadas)')
    plt.plot(xi, yi, 'ro', markersize=10, label='Puntos dados')

    # Dibujar tangentes (derivadas)
    for x, y, dy in zip(xi, yi, dyi):
        x_tang = np.array([x - 0.1, x + 0.1])
        y_tang = y + dy * (x_tang - x)
        plt.plot(x_tang, y_tang, 'r--', alpha=0.5, linewidth=1)

    plt.grid(True, alpha=0.3)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Interpolación de Hermite vs Newton', fontsize=14, fontweight='bold')
    plt.legend()
    plt.tight_layout()
    plt.savefig('hermite.png', dpi=300)
    print(f"\n✅ Gráfica guardada como 'hermite.png'")
    plt.show()


def ejemplo_hermite_funcion_conocida():
    """
    Ejemplo interpolando una función conocida
    """
    print("\n\n" + "=" * 80)
    print("EJEMPLO 2: Interpolando e^x")
    print("=" * 80 + "\n")

    # Función exponencial
    xi = np.array([0, 0.5, 1.0])
    yi = np.exp(xi)  # e^x
    dyi = np.exp(xi)  # d/dx(e^x) = e^x

    print("Puntos para e^x:")
    for x, y, dy in zip(xi, yi, dyi):
        print(f"  x={x:.1f}: f(x)={y:.6f}, f'(x)={dy:.6f}")

    # Interpolar
    z, tabla = hermite_diferencias_divididas(xi, yi, dyi)

    # Evaluar en puntos intermedios 
    x_test = np.array([0.25, 0.75])
    for x in x_test:
        y_interp = hermite_interpolation(xi, yi, dyi, x, z, tabla)
        y_real = np.exp(x)
        error = abs(y_interp - y_real)
        print(f"\nx = {x}:")
        print(f"  Interpolado: {y_interp:.8f}")
        print(f"  Real e^{x} : {y_real:.8f}")
        print(f"  Error:       {error:.2e}")


if __name__ == "__main__":
    ejemplo_hermite()
    ejemplo_hermite_funcion_conocida()