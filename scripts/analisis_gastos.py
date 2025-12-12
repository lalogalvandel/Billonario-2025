import numpy as np

# 1. Definimos tus gastos semestrales como una Matriz (Filas x Columnas)
# Fila 1 = Semestre Primavera (Ene-May)
# Fila 2 = Semestre Otoño (Ago-Dic)
# Columnas = [Colegiatura, Gastos Vida, Sorteo]
gastos_semestre = np.array([
    [41700, 25000, 0],      # Semestre 2 (Sin sorteo, gastos vida aprox 5k/mes)
    [41700, 25000, 20400]   # Semestre 3 (Con sorteo al final del año)
])

print("--- TU MATRIZ DE GASTOS ---")
print(gastos_semestre)

# 2. Suma rápida con Numpy (Cálculo vectorial)
# Sumamos todo el contenido de la matriz de un golpe
total_anual = gastos_semestre.sum()

print(f"\n🔥 GASTO TOTAL PROYECTADO 2026: ${total_anual:,.2f}")

# 3. ¿Sobrevives con los 230k?
capital = 230530
saldo_final = capital - total_anual

print(f"💰 SALDO RESTANTE: ${saldo_final:,.2f}")