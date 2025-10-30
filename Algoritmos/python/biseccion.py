"""
Método de Bisección para encontrar raíces
Divide el intervalo a la mitad repetidamente
Requiere que f(a) y f(b) tengan signos opuestos
"""


def biseccion(f, a, b, tol=1e-6, max_iter=100):
    """
    Método de Bisección

    Parámetros:
    -----------
    f : function
        Función de la cual se busca la raíz
    a, b : float
        Extremos del intervalo inicial [a, b]
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
    # Verificar que f(a) y f(b) tienen signos opuestos
    fa = f(a)
    fb = f(b)

    if fa * fb > 0:
        print("Error: f(a) y f(b) deben tener signos opuestos")
        return None, []

    iteraciones = []

    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        iteraciones.append({
            'n': i,
            'a': a,
            'b': b,
            'c': c,
            'f(a)': fa,
            'f(b)': fb,
            'f(c)': fc,
            'longitud': b - a
        })

        # Criterio de convergencia
        if abs(fc) < tol or (b - a) / 2 < tol:
            print(f"Convergencia alcanzada en {i + 1} iteraciones")
            return c, iteraciones

        # Actualizar intervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    print(f"No se alcanzó convergencia en {max_iter} iteraciones")
    return (a + b) / 2, iteraciones


# Ejemplo de uso
if __name__ == "__main__":
    import math

    # Ejemplo: Encontrar raíz de x^3 - x - 2 = 0 en [1, 2]
    f = lambda x: x ** 3 - x - 2

    raiz, hist = biseccion(f, a=1, b=2)

    if raiz:
        print(f"\nRaíz encontrada: {raiz:.10f}")
        print(f"Verificación f(raíz) = {f(raiz):.2e}")

        print("\nHistorial de iteraciones:")
        for it in hist:
            print(f"n={it['n']}: [{it['a']:.6f}, {it['b']:.6f}] -> c={it['c']:.6f}, f(c)={it['f(c)']:.6f}")