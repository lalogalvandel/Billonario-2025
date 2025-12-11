import matplotlib.pyplot as plt

# 1. Datos del Tiempo (Eje X)
meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

# 2. Datos del Dinero (Eje Y)
# Empezamos con 230k.
# Restamos aprox $12,800 al mes (promedio de tus gastos anuales / 12)
capital = [
    230530, 217730, 204930, 192130, 179330, 166530, 
    153730, 140930, 128130, 115330, 102530, 89730
]

# 3. Configuración de la Gráfica
plt.figure(figsize=(10, 6))  # Tamaño de la imagen
plt.plot(meses, capital, marker='o', color='red', linestyle='--', linewidth=2)

# Decoración (Títulos y etiquetas)
plt.title('RUNWAY 2026: La Caída del Capital', fontsize=16, fontweight='bold')
plt.xlabel('Meses del 2026')
plt.ylabel('Capital Disponible (MXN)')
plt.grid(True, alpha=0.3) # Cuadrícula de fondo

# Línea de peligro (El límite de seguridad)
plt.axhline(y=76000, color='blue', linestyle='-', label='Piso Final ($76k)')
plt.legend()

# 4. Mostrar
print("Generando gráfica...")
plt.show()