import pandas as pd

print("--- 📊 INICIANDO AUDITORÍA AUTOMÁTICA ---")

# 1. CREAMOS LOS DATOS (Imagina que esto viene de un Excel)
datos = {
    'Fecha': ['2025-01-01', '2025-01-02', '2025-01-02', '2025-01-03', '2025-01-03'],
    'Vendedor': ['Lalo', 'Ana', 'Lalo', 'Carlos', 'Ana'],
    'Producto': ['Seguro Vida', 'Seguro Auto', 'Fondo Inv.', 'Seguro Vida', 'Fondo Inv.'],
    'Monto': [15000, 8000, 50000, 15000, 45000]
}

# 2. CONVERTIMOS A DATAFRAME (La magia de Pandas)
df = pd.to_datetime(datos['Fecha']) # Convertimos fechas a formato real
df = pd.DataFrame(datos)

print("\n1. ASÍ SE VEN TUS DATOS EN MEMORIA:")
print(df)

# 3. ANÁLISIS RÁPIDO (Lo que en Excel te tomaría filtros y tablas dinámicas)
print("\n--- 🔍 RESULTADOS DEL ANÁLISIS ---")

# Suma total
total_vendido = df['Monto'].sum()
print(f"💰 Venta Total de la semana: ${total_vendido:,.2f}")

# Promedio de venta
promedio = df['Monto'].mean()
print(f"📉 Ticket Promedio: ${promedio:,.2f}")

# ¿Quién vendió más? (Top Performer)
mejor_vendedor = df.groupby('Vendedor')['Monto'].sum().sort_values(ascending=False)
print("\n🏆 RANKING DE VENDEDORES:")
print(mejor_vendedor)

# 4. EXPORTAR REPORTE (Guardar resultados)
# Esto crea un archivo real en tu carpeta
df.to_csv('semana_2/reporte_auditoria.csv', index=False)
print("\n✅ Reporte guardado como 'reporte_auditoria.csv'")