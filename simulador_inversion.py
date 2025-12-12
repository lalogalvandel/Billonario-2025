print("--- 🔄 SIMULADOR DE BOLA DE NIEVE ---")

saldo_inicial = 230530  # Tu capital real actual
aportacion_mensual = 3000 # Meta: Ganar esto extra en freelancing
tasa_interes = 0.12     # 12% anual (SOFIPO/Cetes mix)
anios = 5

saldo_actual = saldo_inicial

print(f"Inicio: ${saldo_actual:,.2f}")

# AQUÍ ESTÁ LA MAGIA (El Bucle)
for i in range(1, anios + 1):
    # 1. Sumamos lo que ahorraste en el año (aportación x 12)
    saldo_actual = saldo_actual + (aportacion_mensual * 12)
    
    # 2. El dinero genera hijos (interés)
    rendimiento = saldo_actual * tasa_interes
    saldo_actual = saldo_actual + rendimiento
    
    # 3. Imprimimos el corte de caja del año
    print(f"Año {i}: Saldo acumulado: ${saldo_actual:,.2f} (Ganaste ${rendimiento:,.2f} solo por dormir)")