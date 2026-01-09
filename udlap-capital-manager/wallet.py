import os
import json
import shutil 
from datetime import datetime

# --- 1. ANCLAJE DE RUTA ---
DIRECTORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DATOS = os.path.join(DIRECTORIO_SCRIPT, "mi_cartera.json")
ARCHIVO_BACKUP = os.path.join(DIRECTORIO_SCRIPT, "mi_cartera_BACKUP.json")

print(f"📂 Base de Datos: {ARCHIVO_DATOS}")

# --- LIBRERÍAS ---
try:
    import matplotlib.pyplot as plt
    TIENE_MATPLOTLIB = True
except ImportError:
    TIENE_MATPLOTLIB = False

try:
    import pandas as pd
    TIENE_PANDAS = True
except ImportError:
    TIENE_PANDAS = False

# --- NUMPY ---
try:
    import numpy as np
    TIENE_NUMPY = True
except ImportError:
    TIENE_NUMPY = False

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- 2. SISTEMA DE DATOS  ---
def crear_backup():
    if os.path.exists(ARCHIVO_DATOS):
        try: shutil.copy2(ARCHIVO_DATOS, ARCHIVO_BACKUP)
        except: pass

def cargar_datos():
    crear_backup()
    if not os.path.exists(ARCHIVO_DATOS):
        return {"cartera": [], "historial": []}
    try:
        with open(ARCHIVO_DATOS, "r") as archivo:
            datos = json.load(archivo)
            if isinstance(datos, dict):
                if "cartera" not in datos: datos["cartera"] = []
                if "historial" not in datos: datos["historial"] = []
                return datos
            return {"cartera": [], "historial": []}
    except:
        if os.path.exists(ARCHIVO_BACKUP):
            shutil.copy2(ARCHIVO_BACKUP, ARCHIVO_DATOS)
            return cargar_datos()
        return {"cartera": [], "historial": []}

def guardar_datos(datos):
    try:
        with open(ARCHIVO_DATOS, "w") as archivo:
            json.dump(datos, archivo, indent=4)
    except: pass

# --- FUNCIONES BÁSICAS  ---
def registrar_instrumento(datos):
    print("\n--- 🏦 ALTA DE NUEVO ACTIVO ---")
    nombre = input("Nombre (ej. Nu, Cetes): ")
    try: monto = float(input(f"Monto inicial: $"))
    except: return

    if input("¿Genera rendimiento? (s/n): ").lower() == 's':
        try: tasa = float(input("Tasa Anual %: "))
        except: tasa = 0.0
        
        print("Frecuencia de pago: 1.Diario 2.Semanal 3.Mensual 4.Anual")
        freq_op = input("Opción: ")
        frecuencia = {"1":"Diario","2":"Semanal","3":"Mensual","4":"Anual"}.get(freq_op, "Mensual")
        
        if input("¿Tiene tope? (s/n): ").lower() == 's':
            try:
                limite = float(input("Límite: $"))
                tasa_exc = float(input("Tasa Excedente %: "))
                if monto > limite:
                    exc = monto - limite
                    datos["cartera"].append({"nombre": f"{nombre} (Top)", "monto": limite, "tasa": tasa, "frecuencia": frecuencia})
                    datos["cartera"].append({"nombre": f"{nombre} (Exc)", "monto": exc, "tasa": tasa_exc, "frecuencia": frecuencia})
                    guardar_datos(datos); print("✅ Dividido y Guardado."); return
            except: pass
        
        datos["cartera"].append({"nombre": nombre, "monto": monto, "tasa": tasa, "frecuencia": frecuencia})
    else:
        datos["cartera"].append({"nombre": nombre, "monto": monto, "tasa": 0.0, "frecuencia": "N/A"})
    
    guardar_datos(datos); print("✅ Guardado.")

def gestionar_activos(datos):
    while True:
        limpiar_pantalla()
        print("\n--- ⚙️ GESTIÓN ---")
        if not datos["cartera"]: print("Vacío."); input("..."); return

        print(f"{'#':<3} | {'NOMBRE':<15} | {'MONTO':<12}")
        print("-" * 35)
        for i, cta in enumerate(datos["cartera"], 1):
            print(f"{i:<3} | {cta['nombre']:<15} | ${cta['monto']:<11,.2f}")

        print("\n0. Regresar")
        try:
            op = int(input("Selecciona #: "))
            if op == 0: return
            idx = op - 1
            if idx < 0 or idx >= len(datos["cartera"]): continue
            
            act = datos["cartera"][idx]
            print(f"\nEditando: {act['nombre']}")
            print("1. Tasa | 2. Nombre | 3. Monto Manual | 4. Eliminar")
            op2 = input("Opción: ")
            
            if op2 == '1': act['tasa'] = float(input("Nueva Tasa: "))
            elif op2 == '2': act['nombre'] = input("Nuevo Nombre: ")
            elif op2 == '3': act['monto'] = float(input("Nuevo Monto: "))
            elif op2 == '4': 
                if input("¿Borrar? (s/n): ").lower()=='s': datos["cartera"].pop(idx)
            
            guardar_datos(datos)
        except: pass

def registrar_movimiento(datos):
    print("\n--- 💸 FLUJO ---")
    if not datos["cartera"]: print("Vacío."); return
    for i, a in enumerate(datos["cartera"], 1): print(f"{i}. {a['nombre']} (${a['monto']:,.2f})")
    
    try:
        idx = int(input("Cuenta: ")) - 1
        if idx < 0 or idx >= len(datos["cartera"]): return
        cta = datos["cartera"][idx]
        
        tipo = input("1.INGRESO (+) / 2.GASTO (-): ")
        monto = float(input("Monto: $"))
        
        if tipo == '1': 
            cta['monto'] += monto
            etiqueta = "INGRESO"
        elif tipo == '2': 
            cta['monto'] -= monto
            etiqueta = "GASTO"
        else: return

        datos["historial"].append({
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "tipo": etiqueta,
            "monto": monto,
            "cuenta": cta['nombre']
        })
        guardar_datos(datos); print("✅ Hecho.")
    except: pass

def consultar_capital(datos):
    limpiar_pantalla()
    if not datos["cartera"]: print("⚠️ Vacío."); input("..."); return

    total = sum(x['monto'] for x in datos["cartera"])
    renta_anual_total = sum(x['monto'] * (x['tasa']/100) for x in datos["cartera"])

    print(f"\n💰 CAPITAL TOTAL:   ${total:,.2f}")
    if total > 0:
        tasa_ponderada = (renta_anual_total / total) * 100
        print(f"📈 TASA PONDERADA:  {tasa_ponderada:.2f}% Anual")
        print(f"🤑 RENTA MENSUAL:   ${renta_anual_total/12:,.2f} (aprox)")
    
    print("\n" + "="*75)
    print(f"{'INSTRUMENTO':<20} | {'MONTO':>12} | {'TASA':>6} | {'FREQ':<8} | {'% TOTAL':>8}")
    print("-" * 75)
    for x in datos["cartera"]:
        pct = (x['monto'] / total * 100) if total > 0 else 0
        freq = x.get('frecuencia', 'Mensual')[:7]
        print(f"{x['nombre']:<20} | ${x['monto']:>11,.2f} | {x['tasa']:>5}% | {freq:<8} | {pct:>7.2f}%")
    print("="*75)
    input("\nEnter para volver...")

def ver_estado_resultados(datos):
    limpiar_pantalla()
    print("\n--- 📅 ESTADO DE RESULTADOS ---")
    if not datos["historial"]: print("Vacío."); input("..."); return
    if not TIENE_PANDAS: print("Falta Pandas."); input("..."); return

    df = pd.DataFrame(datos["historial"])
    df['fecha_dt'] = pd.to_datetime(df['fecha'])
    df['Periodo'] = df['fecha_dt'].dt.to_period('M')
    
    resumen = df.groupby(['Periodo', 'tipo'])['monto'].sum().unstack(fill_value=0)
    if 'INGRESO' not in resumen.columns: resumen['INGRESO'] = 0.0
    if 'GASTO' not in resumen.columns: resumen['GASTO'] = 0.0
    resumen['UTILIDAD NETA'] = resumen['INGRESO'] - resumen['GASTO']
    
    print(resumen.to_string(float_format=lambda x: f"${x:,.2f}"))
    input("\nEnter...")

def exportar_excel(datos):
    print("\n--- 📊 GENERANDO REPORTES CONTABLES ---")
    if not TIENE_PANDAS: return
    try:
        df_bal = pd.DataFrame(datos["cartera"])
        if not df_bal.empty:
            cols = [c for c in ["nombre", "monto", "tasa", "frecuencia"] if c in df_bal.columns]
            df_bal = df_bal[cols]
            df_bal.columns = ["Cuenta", "Valor", "Tasa", "Frecuencia"]

        df_dia = pd.DataFrame(datos["historial"])
        if not df_dia.empty:
            df_dia = df_dia[["fecha", "cuenta", "tipo", "monto"]]
            df_dia.columns = ["Fecha", "Cuenta", "Tipo", "Monto"]

        df_er = pd.DataFrame()
        if not df_dia.empty:
            df_temp = pd.DataFrame(datos["historial"])
            df_temp['fecha_dt'] = pd.to_datetime(df_temp['fecha'])
            df_temp['Periodo'] = df_temp['fecha_dt'].dt.strftime('%Y-%m')
            df_er = df_temp.pivot_table(index='Periodo', columns='tipo', values='monto', aggfunc='sum', fill_value=0)
            if 'INGRESO' not in df_er: df_er['INGRESO'] = 0
            if 'GASTO' not in df_er: df_er['GASTO'] = 0
            df_er['NETO'] = df_er['INGRESO'] - df_er['GASTO']

        path = os.path.join(DIRECTORIO_SCRIPT, "Estados_Financieros_UDLAP.xlsx")
        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            if not df_bal.empty: df_bal.to_excel(writer, sheet_name="Balance General", index=False)
            if not df_dia.empty: df_dia.to_excel(writer, sheet_name="Libro Diario", index=False)
            if not df_er.empty: df_er.to_excel(writer, sheet_name="Estado de Resultados")
        print(f"✅ Reporte generado: {path}"); input("Enter...")
    except Exception as e: print(f"❌ Error: {e}"); input("Enter...")

def simular_futuro(datos):
    # Simulador Determinista (Clásico)
    limpiar_pantalla()
    print("\n--- 🔮 SIMULADOR LINEAL (Determinista) ---")
    if not datos["cartera"]: input("Sin fondos..."); return
    capital_inicial = sum(x['monto'] for x in datos["cartera"])
    ingreso_pasivo = sum(x['monto']*(x['tasa']/100) for x in datos["cartera"])
    tasa_prom = (ingreso_pasivo/capital_inicial)/12 if capital_inicial > 0 else 0
    
    print(f"Capital: ${capital_inicial:,.2f} | Tasa: {tasa_prom*1200:.2f}%")
    try: costo = float(input("Costo Semestre: $")); ahorro = float(input("Ahorro Mensual: $")); anios = int(input("Años: "))
    except: return
    
    meses = anios * 12
    # Cálculo simple para visualización rápida
    eje_x = list(range(meses + 1))
    saldo = [capital_inicial]
    cap = capital_inicial
    for m in range(1, meses + 1):
        cap += cap * tasa_prom + ahorro
        if m % 6 == 0: cap -= costo # Simplificación semestral
        saldo.append(cap)
        
    if TIENE_MATPLOTLIB:
        plt.figure(figsize=(10,5))
        plt.plot(eje_x, saldo, color='blue', label='Proyección Lineal')
        plt.axhline(y=0, color='red', linestyle='--')
        plt.title("Proyección Estándar"); plt.legend(); plt.show()

# --- LA JOYA DE LA CORONA: MONTECARLO ---
def simular_montecarlo(datos):
    limpiar_pantalla()
    print("\n--- 🎲 SIMULADOR ESTOCÁSTICO (MONTECARLO) ---")
    print("Bienvenido, Actuario. Vamos a calcular el riesgo real.")
    
    if not TIENE_NUMPY:
        print("❌ Error: Necesitas NumPy. Ejecuta: pip install numpy")
        input("Enter..."); return

    if not datos["cartera"]: print("Sin fondos."); input("..."); return

    # 1. Parámetros Base
    capital_inicial = sum(x['monto'] for x in datos["cartera"])
    
    print(f"\nCapital Inicial: ${capital_inicial:,.2f}")
    try:
        ahorro_mensual = float(input("Ahorro mensual extra (Sueldo): $"))
        costo_semestre = float(input("Costo Semestre UDLAP: $"))
        anios = int(input("Años a proyectar: "))
        iteraciones = 1000 # Número estándar para pruebas rápidas
    except: return
    
    # 2. Parámetros de Riesgo (La clave Actuarial)
    print("\n--- CONFIGURACIÓN DE MERCADO ---")
    print("Define el comportamiento de tus inversiones (Renta Variable/Fija):")
    try:
        tasa_media = float(input("Rendimiento Promedio Esperado Anual % (ej. 11): ")) / 100
        volatilidad = float(input("Volatilidad (Desviación Estándar) % (ej. 2 para Cetes, 15 para Crypto): ")) / 100
    except: return

    meses_totales = anios * 12
    dt = 1/12 # Paso de tiempo (mensual)
    
    # Matriz de Simulación: [Iteraciones, Meses]
    # Creamos 1000 caminos posibles
    resultados = np.zeros((iteraciones, meses_totales + 1))
    resultados[:, 0] = capital_inicial

    print(f"\n🔄 Corriendo {iteraciones} simulaciones de futuros posibles...")
    
    for t in range(1, meses_totales + 1):
        # Generamos rendimientos aleatorios para este mes en todos los escenarios
        # Fórmula: Retorno = (Media - 0.5*Vol^2)*dt + Vol*sqrt(dt)*Z
        
        z = np.random.normal(0, 1, iteraciones)
        rendimiento_mes = (tasa_media - 0.5 * volatilidad**2) * dt + volatilidad * np.sqrt(dt) * z
        
        # Actualizamos capitales
        previos = resultados[:, t-1]
        nuevos = previos * np.exp(rendimiento_mes) + ahorro_mensual
        
        # Descuento de colegiatura (Semestral: Enero y Agosto aprox -> cada 6 meses)
        if t % 6 == 0:
            nuevos -= costo_semestre
            
        resultados[:, t] = nuevos

    # 3. Análisis de Resultados (Estadística Descriptiva)
    capitales_finales = resultados[:, -1]
    exitos = np.sum(capitales_finales > 0)
    prob_exito = (exitos / iteraciones) * 100
    promedio_final = np.mean(capitales_finales)
    peor_escenario = np.percentile(capitales_finales, 5) # El 5% más salado
    mejor_escenario = np.percentile(capitales_finales, 95) # El 5% más suertudo

    print("\n" + "="*50)
    print(f"📊 RESULTADOS DEL ANÁLISIS DE RIESGO")
    print("="*50)
    print(f"✅ PROBABILIDAD DE SUPERVIVENCIA: {prob_exito:.1f}%")
    print(f"💰 Capital Promedio Esperado:     ${promedio_final:,.2f}")
    print(f"😨 Peor Escenario (VaR 95%):      ${peor_escenario:,.2f}")
    print(f"🚀 Mejor Escenario (Top 5%):      ${mejor_escenario:,.2f}")
    print("-" * 50)
    
    if prob_exito < 80:
        print("⚠️ ALERTA ACTUARIAL: El riesgo de quiebra es alto.")
        print("   Sugerencia: Aumenta el ahorro mensual o reduce volatilidad.")
    else:
        print("🛡️ SOLIDEZ FINANCIERA: Tu plan es robusto ante la incertidumbre.")

    # 4. Gráfica de Espagueti (Montecarlo Plot)
    if TIENE_MATPLOTLIB:
        plt.figure(figsize=(10, 6))
        # Graficamos solo los primeros 50 caminos para no saturar
        plt.plot(resultados[:50, :].T, color='gray', alpha=0.1)
        # Graficamos el promedio
        plt.plot(np.mean(resultados, axis=0), color='blue', linewidth=2, label='Promedio')
        # Graficamos línea de cero
        plt.axhline(y=0, color='red', linestyle='--')
        
        plt.title(f"Simulación Montecarlo ({iteraciones} escenarios)")
        plt.xlabel("Meses")
        plt.ylabel("Capital")
        plt.legend()
        plt.show()
    
    input("Enter para continuar...")

def menu():
    datos = cargar_datos()
    while True:
        limpiar_pantalla()
        print("=================================")
        print(" 🦅 WALLET v11.0 (ACTUARY ED.)")
        print("=================================")
        print("1. Nuevo Activo")
        print("2. ⚙️ Gestionar")
        print("3. Registrar Flujo")
        print("4. 🔍 Portafolio Detallado")
        print("5. 📅 Estado de Resultados")
        print("6. 🔮 Simulador Lineal")
        print("7. 📊 Excel Contable")
        print("8. 🎲 Simulador Montecarlo (NUEVO)")
        print("9. Salir")
        op = input("\nOpción: ")
        if op=='1': registrar_instrumento(datos)
        elif op=='2': gestionar_activos(datos)
        elif op=='3': registrar_movimiento(datos)
        elif op=='4': consultar_capital(datos)
        elif op=='5': ver_estado_resultados(datos)
        elif op=='6': simular_futuro(datos)
        elif op=='7': exportar_excel(datos)
        elif op=='8': simular_montecarlo(datos)
        elif op=='9': break

if __name__ == "__main__":
    menu()
