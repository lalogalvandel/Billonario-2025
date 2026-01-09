import pandas as pd

print("--- ROBOT AUDITOR INICIADO ---")

# 1. CARGAR DATOS 
# Esto simula cargar un Excel gigante del banco
df = pd.read_csv('semana_2/reporte_auditoria.csv')

print(f" Se cargaron {len(df)} transacciones.")

# 2. DEFINIR REGLA DE AUDITORÍA
# "Muéstrame solo las ventas mayores a $20,000"
limite_sospechoso = 20000

# Esta es la sintaxis de filtrado: df[ condicion ]
transacciones_grandes = df[df['Monto'] > limite_sospechoso]

print(f"\n SE ENCONTRARON {len(transacciones_grandes)} TRANSACCIONES GRANDES:")
print(transacciones_grandes)

# 3. GUARDAR EL REPORTE DE ALERTA
transacciones_grandes.to_csv('semana_2/alerta_auditoria.csv', index=False)
print("\n Reporte de alertas generado: 'alerta_auditoria.csv'")
