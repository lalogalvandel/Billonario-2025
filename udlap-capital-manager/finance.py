# finance.py
# Módulo de Inteligencia Financiera

def calcular_proyeccion_rendimiento(capital_actual, tasa_anual=0.10, meses=11):
    """
    Calcula cuánto dinero tendrás al final del periodo usando interés compuesto.
    Por defecto usamos 10% anual (Finsus/Sofipos) y 11 meses plazo.
    """
    if capital_actual <= 0:
        return 0.0
        
    # Fórmula: M = C * (1 + i/n)^(n*t)
    n = 12
    t = meses / 12
    
    monto_final = capital_actual * (1 + tasa_anual/n)**(n*t)
    ganancia = monto_final - capital_actual
    
    return ganancia

def calcular_costo_oportunidad(meta_total, precio, boletos_vendidos):
    """
    Calcula cuánto dinero "gratis" estás dejando ir por los boletos que NO has vendido.
    """
    boletos_pendientes = meta_total - boletos_vendidos
    dinero_parado = boletos_pendientes * precio
    
    # ¿Cuánto ganarías si tuvieras ese dinero hoy invertido?
    interes_perdido = calcular_proyeccion_rendimiento(dinero_parado)
    
    return interes_perdido
