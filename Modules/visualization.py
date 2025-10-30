#Código encargado de la generación de gráficas

import matplotlib.pyplot as plt

# Datos
x = [0, 5,10,15,20,25,30,35,40,45,50,55]
y = [22.1,23.5,25.8,27.3,28.9,30.2,29.8,28.5,26.7,25.1,23.8,22.5]

# Crear la gráfica
plt.scatter(x, y, color='orange', label='Datos experimentales')  # Puntos
plt.plot(x, y, color='gray', linestyle='--', alpha=0.5)         # Línea guía opcional

# Decoración
plt.title("Gráfica de datos experimentales")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()
