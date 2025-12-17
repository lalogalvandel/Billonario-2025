import os
import json
from datetime import datetime

# Intentamos importar matplotlib para las gráficas
try:
    import matplotlib.pyplot as plt
    TIENE_MATPLOTLIB = True
except ImportError:
    TIENE_MATPLOTLIB = False

ARCHIVO_DATOS = "mi_cartera.json"

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- PERSISTENCIA ---
def cargar_datos():
    if not os.path.exists(ARCHIVO_DATOS):
        return {"cartera": [], "historial": []}
    try:
        with open(ARCHIVO_DATOS, "r") as archivo:
            datos = json.load(archivo)
            if isinstance(datos, list): return {"cartera": datos, "historial": []}
            return datos
    except:
        return {"cartera": [], "historial": []}

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w") as archivo:
        json.dump(datos, archivo, indent=4)

# --- FUNCIONES BÁSICAS (Registro y Consulta) ---
def registrar_instrumento(datos):
    print("\n--- 🏦 REGISTRAR INSTRUMENTO ---")
    nombre = input("Nombre (ej. Nu, Cetes): ")
    try:
        monto = float(input(f"Monto total en {nombre}: $"))
    except:
        print("Error en número."); return

    if input("¿Genera rendimiento? (s/n): ").lower() == 's':
        tasa = float(input("Tasa Anual (%): "))
        print("Pago: 1.Diario 2.Semanal 3.Mensual 4.Anual")
        freq = input("Opción: ")
        frecuencia = {"1":"Diario","2":"Semanal","3":"Mensual","4":"Anual"}.get(freq, "Mensual")
        
        if input("¿Tiene tope? (s/n): ").lower() == 's':
            limite = float(input("Límite del tope: $"))
            if monto > limite:
                exc = monto - limite
                tasa2 = float(input(f"Tasa del excedente (${exc}): "))
                datos["cartera"].append({"nombre":f"{nombre} (Top)", "monto":limite, "tasa":tasa, "frecuencia":frecuencia})
                datos["cartera"].append({"nombre":f"{nombre} (Exc)", "monto":exc, "tasa":tasa2, "frecuencia":frecuencia})
            else:
                datos["cartera"].append({"nombre":nombre, "monto":monto, "tasa":tasa, "frecuencia":frecuencia})
        else:
            datos["cartera"].append({"nombre":nombre, "monto":monto, "tasa":tasa, "frecuencia":frecuencia})
    else:
        datos["cartera"].append({"nombre":nombre, "monto":monto, "tasa":0.0, "frecuencia":"N/A"})
    
    guardar_datos(datos); print("✅ Guardado.")

def registrar_movimiento(datos):
    print("\n--- 💸 CASH FLOW ---")
    if not datos["cartera"]: return
    for i, a in enumerate(datos["cartera"], 1): print(f"{i}. {a['nombre']} (${a['monto']:,.2f})")
    try:
        idx = int(input("Cuenta: ")) - 1
        cta = datos["cartera"][idx]
        tipo = input("1.INGRESO / 2.GASTO: ")
        monto = float(input("Monto: $"))
        if tipo=='1': cta['monto']+=monto
        elif tipo=='2': cta['monto']-=monto
        datos["historial"].append({"fecha":datetime.now().strftime("%Y-%m-%d"),"tipo":"INGRESO" if tipo=='1' else "GASTO","monto":monto,"cuenta":cta['nombre']})
        guardar_datos(datos); print("✅ Hecho.")
    except: pass

def consultar_capital(datos):
    limpiar_pantalla()
    total = sum(x['monto'] for x in datos["cartera"])
    renta = sum((x['monto']*(x['tasa']/100))/12 for x in datos["cartera"])
    print(f"\n💰 CAPITAL: ${total:,.2f} | 🤑 RENTA MENSUAL: ${renta:,.2f}")
    input("Enter...")

# --- EL CEREBRO FINANCIERO (SIMULADOR) ---
def simular_futuro(datos):
    limpiar_pantalla()
    print("\n--- 🔮 ORÁCULO FINANCIERO UDLAP (v5.0) ---")
    if not TIENE_MATPLOTLIB: print("Error: Instala matplotlib."); return
    if not datos["cartera"]: print("Registra dinero primero."); return

    # 1. Estado Inicial
    capital_inicial = sum(x['monto'] for x in datos["cartera"])
    ingreso_pasivo_anual = sum(x['monto'] * (x['tasa']/100) for x in datos["cartera"])
    tasa_promedio_mensual = (ingreso_pasivo_anual / capital_inicial) / 12 if capital_inicial > 0 else 0
    
    print(f"💵 Capital Inicial: ${capital_inicial:,.2f}")
    print(f"📈 Rendimiento Promedio de tu Portafolio: {tasa_promedio_mensual*100*12:.2f}% Anual")

    # 2. Configuración de Gastos
    print("\n--- GASTOS UNIVERSITARIOS ---")
    costo_semestre = float(input("Costo del Semestre (Precio de Contado): $"))
    
    print("\n¿Cómo planeas pagar?")
    print("1. DE CONTADO (1 pago al inicio del semestre)")
    print("2. FINANCIADO (4 pagos: Ene-Abr y Ago-Nov con 3.2% interés mensual)")
    modo_pago = input("Elige (1 o 2): ")

    ahorro_actual = float(input("\nIngreso/Ahorro extra mensual ACTUAL (Si no tienes, pon 0): $"))
    anios = int(input("Años a proyectar (ej. 4): "))
    meses_totales = anios * 12

    # --- LÓGICA DE PAGOS ---
    # Meses de pago semestre 1: Enero(1), Febrero(2), Marzo(3), Abril(4) -> Índices 0,1,2,3 (aprox, asumiendo inicio en Enero)
    # Meses de pago semestre 2: Agosto(8)... -> Índices 7,8,9,10
    
    # Si es financiado, calculamos el golpe mensual con el recargo
    # Simplificación: 3.2% mensual sobre el saldo.
    # Asumimos que divides el costo en 4, y cada mes pagas capital + interés.
    # Para simplificar la simulación visual: Asumiremos un sobrecosto total aprox del 10-12% semestral si se financia.
    # Pero usaremos tu dato: 4 pagos.
    if modo_pago == '2':
        # Cálculo rápido de cuota financiada (Interés simple sobre saldo para no complicar en exceso)
        # Costo total financiado aprox sube un 12.8% si es 3.2% mensual x 4 meses flat, 
        # o menos si es sobre saldos insolutos. Usaremos un factor de seguridad.
        # Vamos a suponer que cada pago mensual es: (Costo / 4) * 1.032
        pago_mensual_uni = (costo_semestre / 4) * 1.032
        print(f"⚠️ Al financiarte, pagarás aprox ${pago_mensual_uni:,.2f} x 4 meses.")
        print(f"   Costo total semestral sube de ${costo_semestre:,.0f} a ${pago_mensual_uni*4:,.0f} (Te cuesta +${(pago_mensual_uni*4)-costo_semestre:,.0f})")
    else:
        pago_mensual_uni = costo_semestre

    # 3. BUSCADOR DEL NÚMERO MÁGICO (Algoritmo de Fuerza Bruta)
    # Buscamos cuánto dinero extra necesitas para terminar con EL MISMO capital que empezaste (Sostenibilidad)
    
    ingreso_necesario = 0
    capital_final_simulado = -1
    
    print("\n🔄 Calculando cuánto necesitas vender para sobrevivir...")
    
    while capital_final_simulado < capital_inicial:
        ingreso_necesario += 100 # Probamos subiendo de 100 en 100
        
        # Simulación rápida interna
        temp_cap = capital_inicial
        for m in range(1, meses_totales + 1):
            # Intereses ganados
            temp_cap += temp_cap * tasa_promedio_mensual
            # Ingreso (Ahorro actual + Lo que estamos probando)
            temp_cap += (ahorro_actual + ingreso_necesario)
            
            # Gasto Uni
            mes_calendario = m % 12 
            if mes_calendario == 0: mes_calendario = 12
            
            if modo_pago == '1': # Contado (Enero y Agosto)
                if mes_calendario == 1 or mes_calendario == 8:
                    temp_cap -= costo_semestre
            else: # Financiado (Ene-Abr y Ago-Nov)
                if mes_calendario in [1, 2, 3, 4, 8, 9, 10, 11]:
                    temp_cap -= pago_mensual_uni
        
        capital_final_simulado = temp_cap
        if ingreso_necesario > 50000: break # Evitar bucle infinito

    print(f"\n🎯 ¡NÚMERO MÁGICO ENCONTRADO!")
    print(f"   Necesitas generar ADICIONALMENTE: ${ingreso_necesario:,.2f} / mes")
    print(f"   (Encima de tus ${ahorro_actual:,.2f} actuales)")

    # 4. GENERACIÓN DE GRÁFICAS DETALLADAS
    eje_x = list(range(meses_totales + 1))
    
    # Escenario A: Realidad Actual (Sin ingresos extra)
    saldo_actual = [capital_inicial]
    cap = capital_inicial
    for m in range(1, meses_totales + 1):
        cap += cap * tasa_promedio_mensual # Rendimiento
        cap += ahorro_actual               # Ahorro actual
        
        # Resta Colegiatura
        mes_cal = m % 12; 
        if mes_cal == 0: mes_cal = 12
        
        if modo_pago == '1':
            if mes_cal == 1 or mes_cal == 8: cap -= costo_semestre
        else:
            if mes_cal in [1,2,3,4,8,9,10,11]: cap -= pago_mensual_uni
            
        saldo_actual.append(cap)

    # Escenario B: Solución (Con el Ingreso Mágico)
    saldo_solucion = [capital_inicial]
    cap = capital_inicial
    for m in range(1, meses_totales + 1):
        cap += cap * tasa_promedio_mensual
        cap += ahorro_actual + ingreso_necesario # <--- AQUÍ ESTÁ LA SOLUCIÓN
        
        mes_cal = m % 12; 
        if mes_cal == 0: mes_cal = 12
        
        if modo_pago == '1':
            if mes_cal == 1 or mes_cal == 8: cap -= costo_semestre
        else:
            if mes_cal in [1,2,3,4,8,9,10,11]: cap -= pago_mensual_uni
            
        saldo_solucion.append(cap)

    # Plotting
    plt.figure(figsize=(12, 7))
    
    # Línea Roja (Peligro) o Amarilla
    color_actual = 'red' if saldo_actual[-1] < 0 else 'orange'
    plt.plot(eje_x, saldo_actual, label=f'Escenario Actual (Ahorro ${ahorro_actual})', color=color_actual, linewidth=2)
    
    # Línea Verde (Éxito)
    plt.plot(eje_x, saldo_solucion, label=f'META: Generando +${ingreso_necesario}/mes', color='green', linewidth=3)
    
    # Línea de Cero (Quiebra)
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    plt.title(f"Plan de Supervivencia Universitaria ({anios} años)", fontsize=14)
    plt.xlabel("Meses")
    plt.ylabel("Capital (MXN)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    txt_final = f"Meta Mensual Extra:\n${ingreso_necesario:,.2f}"
    plt.text(meses_totales + 1, saldo_solucion[-1], txt_final, color='green', fontweight='bold')

    plt.tight_layout()
    plt.show()

def menu():
    datos = cargar_datos()
    while True:
        limpiar_pantalla()
        print("=================================")
        print("   UDLAP TUITION MANAGER v5.0")
        print("=================================")
        print("1. Registrar Fondos/Cuentas")
        print("2. Registrar Movimiento")
        print("3. Ver Capital Total")
        print("4. 🔮 Calcular 'Número Mágico' y Proyectar")
        print("5. Salir")
        op = input("\nOpción: ")
        if op=='1': registrar_instrumento(datos)
        elif op=='2': registrar_movimiento(datos)
        elif op=='3': consultar_capital(datos)
        elif op=='4': simular_futuro(datos)
        elif op=='5': break

if __name__ == "__main__":
    menu()