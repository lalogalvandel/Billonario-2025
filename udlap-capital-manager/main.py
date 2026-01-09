import data  
import crm   
import finance 
import os    

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def ejecutar_sistema():
    limpiar_pantalla()
    print(".........................................")
    print("   UDLAP CAPITAL MANAGER v2.0")
    print(".........................................")
    
    # 1. CÁLCULOS CRM
    reporte = crm.generar_reporte_financiero(data.lista_contactos, data.PRECIO_BOLETO, data.META_TOTAL)
    
    print("\nESTADO DE VENTAS:")
    print(f"   > Vendidos:      {reporte['vendidos']} / {data.META_TOTAL}")
    print(f"   > Cash Flow:     ${reporte['cash_flow']:,.2f}")
    print(f"   > Por Cobrar:    ${reporte['por_cobrar']:,.2f}")
    
    if reporte['por_cobrar'] > 0:
        print(f"   ⚠️  TIENES ${reporte['por_cobrar']:,.2f} EN LA CALLE. ¡COBRA YA!")

    # 2. PROYECCIÓN DE RIQUEZA (NUEVO)
    # Calculamos cuánto ganarás con lo que ya tienes
    ganancia_futura = finance.calcular_proyeccion_rendimiento(reporte['cash_flow'])
    
    # Calculamos cuánto estás perdiendo por no vender los demás
    dinero_perdido = finance.calcular_costo_oportunidad(data.META_TOTAL, data.PRECIO_BOLETO, reporte['vendidos'])

    print("\n PROYECCIÓN DE INVERSIÓN (Finsus/Cetes):")
    print(f"   > Ganancia asegurada (Nov '26):  +${ganancia_futura:,.2f} MXN")
    print(f"   > Costo de Oportunidad (Perdido): -${dinero_perdido:,.2f} MXN")
    print("     (Esto es lo que dejas de ganar por no vender hoy)")

    print("\n" + "-"*40)

    # 3. LISTA DE ATAQUE
    print("\n GENERADOR DE OPORTUNIDADES")
    print("   ¿A quién quieres contactar hoy?")
    print("   1. Lista Caliente (Familia)")
    print("   2. Lista Tibia (Conocidos)")
    print("   3. Lista Fría (Lejanos)")
    
    opcion = input("\n   Elige (1-3): ")
    tipo_map = {"1": "Caliente", "2": "Tibio", "3": "Frio"}
    seleccion = tipo_map.get(opcion)

    if seleccion:
        candidatos = crm.filtrar_por_tipo(data.lista_contactos, seleccion)
        print(f"\n    CANDIDATOS ({seleccion.upper()}):")
        for i, persona in enumerate(candidatos, 1):
            status = "✅ PAGADO" if persona["estado_pago"] else "❌ DEBE COBRAR"
            print(f"      {i}. {persona['nombre']} | {status}")
            if not persona["estado_pago"]:
                 print(f"         Llamar a: {persona['telefono']}")

# Ejecutar
if __name__ == "__main__":
    ejecutar_sistema()
