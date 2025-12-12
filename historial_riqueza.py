# Lista vacía (La mochila está vacía al inicio)
historial = []

saldo = 230530
aportacion = 3000
interes = 0.12

print("Calculando y guardando datos...")

# El mismo bucle, pero ahora con memoria
for i in range(1, 6):
    saldo = saldo + (aportacion * 12)
    saldo = saldo + (saldo * interes)
    
    # ¡AQUÍ ESTÁ EL TRUCO!
    # Guardamos el dato en la lista en lugar de solo imprimirlo
    historial.append(saldo) 

print("\n--- DATOS GUARDADOS EN MEMORIA ---")
print(historial)

# Accediendo a datos específicos
print(f"\nEl saldo del Año 3 será: ${historial[2]:,.2f}") 
# (Nota: En Python se cuenta desde 0, por eso el año 3 es el índice 2)