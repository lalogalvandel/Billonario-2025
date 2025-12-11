# Calculadora de Interés Compuesto para Lalo

print("--- 💰 GENERADOR DE RIQUEZA 1.0 ---")

# 1. Inputs (Entrada de datos)
# float() convierte el texto a número decimal
capital = float(input("¿Cuánto dinero vas a invertir hoy?: $"))
tasa = float(input("¿Cuál es la tasa de interés anual (%)?: "))
anios = int(input("¿Por cuántos años lo dejarás crecer?: "))

# 2. Lógica (La fórmula matemática)
# En Python, la potencia se escribe con **
monto_final = capital * ((1 + (tasa / 100)) ** anios)
ganancia = monto_final - capital

# 3. Output (Resultados)
# La 'f' antes de las comillas permite meter variables dentro del texto con {}
print("\n--- RESULTADOS ---")
print(f"En {anios} años tendrás: ${monto_final:,.2f}")
print(f"Tu ganancia neta fue de: ${ganancia:,.2f}")