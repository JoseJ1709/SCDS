"""
Método de Punto Fijo para encontrar raíces
Convierte f(x) = 0 en x = g(x) y aplica x_{n+1} = g(x_n)
"""


def punto_fijo(g, x0, tol=1e-6, max_iter=100):
    """
    Método de Punto Fijo

    Parámetros:
    -----------
    g : function
        Función de iteración g(x) tal que x = g(x)
    x0 : float
        Aproximación inicial
    tol : float
        Tolerancia para el criterio de parada
    max_iter : int
        Número máximo de iteraciones

    Retorna:
    --------
    raiz : float
        Aproximación de la raíz
    iteraciones : list
        Historial de iteraciones
    """
    iteraciones = []
    x = x0

    for i in range(max_iter):
        x_nuevo = g(x)

        iteraciones.append({
            'n': i,
            'x': x,
            'g(x)': x_nuevo,
            'error': abs(x_nuevo - x)
        })

        # Criterio de convergencia
        if abs(x_nuevo - x) < tol:
            print(f"Convergencia alcanzada en {i + 1} iteraciones")
            return x_nuevo, iteraciones

        x = x_nuevo

    print(f"No se alcanzó convergencia en {max_iter} iteraciones")
    return x, iteraciones


# Ejemplo de uso
if __name__ == "__main__":
    import math

    # Ejemplo: Encontrar raíz de x^2 - 2 = 0
    # Reescribimos como x = sqrt(2*x - x^2 + 2) o x = (x^2 + 2)/2x
    # O más simple: x = sqrt(2)  -> g(x) = (x + 2/x)/2
    g = lambda x: (x + 2 / x) / 2

    raiz, hist = punto_fijo(g, x0=1.0)

    if raiz:
        print(f"\nRaíz encontrada: {raiz:.10f}")
        print(f"Verificación: sqrt(2) = {math.sqrt(2):.10f}")

        print("\nHistorial de iteraciones:")
        for it in hist[-5:]:  # Últimas 5 iteraciones
            print(f"n={it['n']}: x={it['x']:.10f}, error={it['error']:.2e}")