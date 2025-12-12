import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

print("--- 🤖 ENTRENANDO IA DE SUELDOS ---")

# 1. DATOS (El pasado)
# X = Años de experiencia (Tiene que ser una matriz, por eso los corchetes dobles)
X = np.array([[0], [1], [2], [3], [4], [5]]) 
# Sueldo: Empieza bajo, se estanca un poco, y luego EXPLOTA hacia arriba
y = np.array([5, 6, 7, 8, 25, 40])

# 2. EL CEREBRO (El Modelo)
modelo = LinearRegression()

# 3. ENTRENAMIENTO (Fit)
# Aquí la IA aprende la relación entre Experiencia y Sueldo
modelo.fit(X, y)

print("¡IA Entrenada!")

# 4. PREDICCIÓN (El Futuro)
# ¿Cuánto debería ganar Lalo en 2 años?
años_lalo = np.array([[2.5]]) # 2 años y medio
prediccion = modelo.predict(años_lalo)

print(f"\nSi tienes {años_lalo[0][0]} años de experiencia...")
print(f"La IA dice que deberías cobrar: ${prediccion[0]:,.2f} miles")

# 5. VISUALIZACIÓN (Para ver qué hizo la IA)
plt.scatter(X, y, color='blue', label='Datos Reales') # Puntos
plt.plot(X, modelo.predict(X), color='red', label='Línea de la IA') # La línea que aprendió
plt.scatter(años_lalo, prediccion, color='green', marker='X', s=200, label='Tu Predicción') # Tú

plt.title('Sueldo vs Experiencia')
plt.xlabel('Años')
plt.ylabel('Sueldo (k)')
plt.legend()
plt.show()