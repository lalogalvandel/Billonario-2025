print("--- 🔄 SIMULADOR DE BOLA DE NIEVE ---")

saldo_inicial = 230530  
aportacion_mensual = 3000 
tasa_interes = 0.12   
anios = 5

saldo_actual = saldo_inicial

print(f"Inicio: ${saldo_actual:,.2f}")

# AQUÍ ESTÁ LA MAGIA (El Bucle)
for i in range(1, anios + 1):
    
    saldo_actual = saldo_actual + (aportacion_mensual * 12)
    
    
    rendimiento = saldo_actual * tasa_interes
    saldo_actual = saldo_actual + rendimiento
    
    
    print(f"Año {i}: Saldo acumulado: ${saldo_actual:,.2f} (Ganaste ${rendimiento:,.2f} solo por dormir)")
