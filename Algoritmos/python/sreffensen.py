"""
Método de Steffensen (o Aitken) para encontrar raíces
Acelera la convergencia del método de punto fijo
Usa la fórmula de Aitken: x_{n+1} = x_n - [g(x_n) - x_n]^2 / [g(g(x_n)) - 2g(x_n) + x_n]
"""


def steffensen(g, x0, tol=1e-6, max_iter=100):
    """
    Método de Steffensen

    Parámetros:
    -----------
    g : function
        Función de iteración de punto fijo
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
        gx = g(x)
        ggx = g(gx)

        # Calcular denominador para Aitken
        denominador = ggx - 2 * gx + x

        # Verificar división por cero
        if abs(denominador) < 1e-10:
            print(f"Error: División por cero en iteración {i}")
            # Intentar continuar con punto fijo simple
            x_nuevo = gx
        else:
            # Fórmula de Steffensen
            x_nuevo = x - (gx - x) ** 2 / denominador

        iteraciones.append({
            'n': i,
            'x': x,
            'g(x)': gx,
            'g(g(x))': ggx,
            'x_nuevo': x_nuevo,
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
    # Usamos g(x) = (x + 2/x) / 2
    g = lambda x: (x + 2 / x) / 2

    raiz, hist = steffensen(g, x0=1.0)

    if raiz:
        print(f"\nRaíz encontrada: {raiz:.10f}")
        print(f"Valor real: sqrt(2) = {math.sqrt(2):.10f}")

        print("\nHistorial de iteraciones:")
        for it in hist:
            print(f"n={it['n']}: x={it['x']:.10f}, x_nuevo={it['x_nuevo']:.10f}, error={it['error']:.2e}")