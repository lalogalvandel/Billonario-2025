# crm.py
# Módulo de Gestión de Relaciones con Clientes
# Aquí está la lógica para filtrar y analizar tu base de datos.

def filtrar_por_tipo(base_datos, tipo_buscado):
    """
    Recibe la lista completa y devuelve solo los contactos del tipo especificado.
    Ej: tipo_buscado = "Caliente"
    """
    lista_filtrada = []
    
    for persona in base_datos:
        # Comparamos ignorando mayúsculas/minúsculas para evitar errores
        if persona["tipo"].lower() == tipo_buscado.lower():
            lista_filtrada.append(persona)
            
    return lista_filtrada

def generar_reporte_financiero(base_datos, precio_boleto, meta_total_boletos):
    """
    Calcula las métricas clave de tu negocio.
    """
    boletos_vendidos = 0
    dinero_recaudado = 0  # Cash Flow Real (En mano)
    dinero_pendiente = 0  # Cuentas por cobrar
    
    for persona in base_datos:
        # Asumimos que cada contacto compra 1 boleto por ahora
        # Busca la clave "boletos", si no la encuentra, asume que es 1
        cantidad = persona.get("boletos", 1)
        
        if persona["estado_pago"] == True:
            boletos_vendidos += cantidad
            dinero_recaudado += (cantidad * precio_boleto)
        else:
            # Si no ha pagado, cuenta como deuda potencial
            dinero_pendiente += (cantidad * precio_boleto)

    # Cálculo de faltantes
    boletos_restantes = meta_total_boletos - boletos_vendidos
    dinero_meta_total = meta_total_boletos * precio_boleto
    progreso_porcentaje = (dinero_recaudado / dinero_meta_total) * 100

    # Devolvemos un diccionario con todas las estadísticas listas
    reporte = {
        "vendidos": boletos_vendidos,
        "restantes": boletos_restantes,
        "cash_flow": dinero_recaudado,
        "por_cobrar": dinero_pendiente,
        "progreso": round(progreso_porcentaje, 2)
    }
    
    return reporte