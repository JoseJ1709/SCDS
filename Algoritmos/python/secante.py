"""
Método de la Secante para encontrar raíces
Aproxima la derivada usando diferencias finitas
Fórmula: x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))
"""


def secante(f, x0, x1, tol=1e-6, max_iter=100):
    """
    Método de la Secante

    Parámetros:
    -----------
    f : function
        Función de la cual se busca la raíz
    x0, x1 : float
        Dos aproximaciones iniciales
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
    x_ant = x0
    x_act = x1

    for i in range(max_iter):
        f_ant = f(x_ant)
        f_act = f(x_act)

        # Verificar división por cero
        if abs(f_act - f_ant) < 1e-10:
            print(f"Error: División por cero en iteración {i}")
            return None, iteraciones

        x_nuevo = x_act - f_act * (x_act - x_ant) / (f_act - f_ant)

        iteraciones.append({
            'n': i,
            'x_{n-1}': x_ant,
            'x_n': x_act,
            'f(x_{n-1})': f_ant,
            'f(x_n)': f_act,
            'x_{n+1}': x_nuevo,
            'error': abs(x_nuevo - x_act)
        })

        # Criterio de convergencia
        if abs(x_nuevo - x_act) < tol:
            print(f"Convergencia alcanzada en {i + 1} iteraciones")
            return x_nuevo, iteraciones

        x_ant = x_act
        x_act = x_nuevo

    print(f"No se alcanzó convergencia en {max_iter} iteraciones")
    return x_act, iteraciones


# Ejemplo de uso
if __name__ == "__main__":
    import math

    # Ejemplo: Encontrar raíz de cos(x) - x = 0
    f = lambda x: math.cos(x) - x

    raiz, hist = secante(f, x0=0, x1=1)

    if raiz:
        print(f"\nRaíz encontrada: {raiz:.10f}")
        print(f"Verificación f(raíz) = {f(raiz):.2e}")

        print("\nHistorial de iteraciones:")
        for it in hist:
            print(f"n={it['n']}: x_n={it['x_n']:.6f}, x_{{n+1}}={it['x_{n+1}']:.6f}, error={it['error']:.2e}")