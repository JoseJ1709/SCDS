# código para aplicar todos los métodos de interpolación.
# a partir de los datos generados para buscar el de mayor precisión

import Algoritmos.interpolacion.python.lagrange as lagrange
from Algoritmos.interpolacion.python.diferenciasdiv import newton_interpolation
from Algoritmos.interpolacion.python.trazadorescub import trazadores_cubicos_naturales, evaluar_spline
import numpy as np

#Retorno: Valores de las interpolaciones en orden: Lagrange, Newton, Trazadores cúbicos
def interpolacion(xi, yi, x):
    """
    Aplica todos método de interpolación a los datos dados
    y verificar cual es el método con mejor precisión y retornarlo.

    Parámetros:
    xi : array_like
        Puntos x conocidos.
    yi : array_like
        Valores y conocidos en los puntos xi.
    x : array_like
        Puntos x donde se desea evaluar la interpolación.
    metodo : str
        Método de interpolación a utilizar ('lagrange', 'newton', 'spline').

    Retorna:
    y : array_like
        Valores interpolados en los puntos x.
    """

    #Interpolación de Lagrange

    yLagrange = lagrange.lagrange_interpolation(xi, yi, x)
    print("Interpolación de Lagrange realizada.")
    print("valor de y en x:", yLagrange)

    #Interpolación de Newton
    yNewton = newton_interpolation(xi, yi, x, None)
    
    print("Interpolación de Newton realizada.")
    print("valor de y en x:", yNewton)


    #Trazadores cúbicos
    coef = trazadores_cubicos_naturales(xi, yi)

    # Evaluar en x
    yTrazadorCubico = evaluar_spline(xi, coef, x)

    print("Trazadores cúbicos realizado")
    print("valor de y en x:", yTrazadorCubico)

    #Retornar los resultados
    return yLagrange, yNewton, yTrazadorCubico



#Comparar precisión de los métodos usando validación cruzada Leave-One-Out
#Retorno: El mejor método de interpolación  para el conjunto de datos
def evaluar_precision(xi, yi):
    n = len(xi)
    errores = {'lagrange': [], 'newton': [], 'spline': []}

    for i in range(n):
        # Separar punto de prueba
        xTrain = xi[:i] + xi[i+1:]
        yTrain = yi[:i] + yi[i+1:]
        xTest = xi[i]
        yReal = yi[i]

        # Lagrange
        y_pred_l = lagrange.lagrange_interpolation(xTrain, yTrain, xTest)
        errores['lagrange'].append(abs(yReal - y_pred_l))

        # Newton
        y_pred_n = newton_interpolation(xTrain, yTrain, xTest)
        errores['newton'].append(abs(yReal - y_pred_n))

        # Spline
        coef = trazadores_cubicos_naturales(xTrain, yTrain)
        y_pred_s = evaluar_spline(xTrain, coef, xTest)
        errores['spline'].append(abs(yReal - y_pred_s))

    # Calcular error promedio (MAE)
    for metodo, e in errores.items():
        print(f"{metodo:10s} → Error medio: {np.mean(e):.15f}")

    # Método con menor error
    mejor = min(errores, key=lambda k: np.mean(errores[k]))
    print(f"\nEl método más preciso es: {mejor.upper()}")
    #Retornar el método más preciso
    return mejor
#-----------------------------------------------------------------------------------------------
# Uso
# nodos (xi) — ya ordenados ascendentemente
x = [0.024076, 0.215298, 0.590394, 1.134948, 1.828034, 2.643016, 3.548577,
     4.509914, 5.490086, 6.451423, 7.356984, 8.171966, 8.865052, 9.409606,
     9.784702, 9.975924]

# valores medidos (yi) correspondientes (semilla fija para reproducibilidad)
y = [19.935694, 20.085081, 20.787186, 22.241118, 23.245721, 24.262249,
     25.051342, 24.770800, 24.207606, 22.976107, 20.940634, 19.318913,
     18.337140, 17.215214, 16.483467, 16.346980]



interpolacion(x, y, 12)
# Comparar resultados y retornar el más preciso
evaluar_precision(x, y)
