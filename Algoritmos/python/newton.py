"""
Método de Newton-Raphson para encontrar raíces de funciones
Fórmula: x_{n+1} = x_n - f(x_n)/f'(x_n)
"""


def newton(f, df, x0, tol=1e-6, max_iter=100):
    """
    Método de Newton-Raphson

    Parámetros:
    -----------
    f : function
        Función de la cual se busca la raíz
    df : function
        Derivada de la función f
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
        fx = f(x)
        dfx = df(x)

        # Verificar división por cero
        if abs(dfx) < 1e-10:
            print(f"Error: Derivada muy pequeña en iteración {i}")
            return None, iteraciones

        x_nuevo = x - fx / dfx

        iteraciones.append({
            'n': i,
            'x': x,
            'f(x)': fx,
            "f'(x)": dfx,
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

    # Ejemplo: Encontrar raíz de f(x) = x^2 - 2 (raíz de 2)
    f = lambda x: x ** 2 - 2
    df = lambda x: 2 * x

    raiz, hist = newton(f, df, x0=1.0)

    if raiz:
        print(f"\nRaíz encontrada: {raiz:.10f}")
        print(f"Verificación f(raíz) = {f(raiz):.2e}")

        print("\nHistorial de iteraciones:")
        for it in hist:
            print(f"n={it['n']}: x={it['x']:.6f}, f(x)={it['f(x)']:.6f}, error={it['error']:.2e}")
