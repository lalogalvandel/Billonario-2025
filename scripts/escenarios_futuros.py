def calcular_riqueza(aporte_mensual):
    """
    Esta función recibe cuánto ahorras al mes
    y te regresa con cuánto terminas en 5 años.
    """
    saldo = 230530
    tasa = 0.12
    anios = 5
    
    for i in range(anios):
        saldo = saldo + (aporte_mensual * 12)
        saldo = saldo + (saldo * tasa)
        
    return saldo  

# --- ZONA DE PRUEBAS ---


escenario_triste = calcular_riqueza(0)


escenario_realista = calcular_riqueza(3000)


escenario_billonario = calcular_riqueza(8000)

print(f"1. Si no hago nada: ${escenario_triste:,.2f}")
print(f"2. Si genero $3k:   ${escenario_realista:,.2f}")
print(f"3. Si genero $8k:   ${escenario_billonario:,.2f}")

diferencia = escenario_billonario - escenario_triste
print(f"\n💡 VALOR DE TU ESFUERZO: ${diferencia:,.2f}")
