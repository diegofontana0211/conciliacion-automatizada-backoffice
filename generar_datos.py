import pandas as pd
import random

random.seed(42)

activos = {
    'AL30': 60000.0,
    'GD30': 65000.0,
    'YPFD': 32000.0,
    'GGAL': 5200.0,
    'PAMP': 3100.0
}

data_byma = []

for i in range(1, 101):
    id_boleto = 500000 + i
    especie = random.choice(list(activos.keys()))
    cantidad = random.choice([100, 500, 1000, 5000, 10000])
    precio_unitario = activos[especie] * random.uniform(0.98, 1.02)
    monto_total = round(cantidad * precio_unitario, 2)
    
    data_byma.append({
        'id_boleto': id_boleto,
        'especie': especie,
        'cantidad': cantidad,
        'precio_unitario': round(precio_unitario, 2),
        'monto_total': monto_total
    })

df_byma = pd.DataFrame(data_byma)
# GUARDAR COMO EXCEL REAL (Columna A, B, C, D, E independientes)
df_byma.to_excel('operaciones_byma.xlsx', index=False)

df_banco = df_byma.copy()

# Error 1: Fuga de información
df_banco = df_banco.drop(15)

# Error 2: Error de tipeo
df_banco.loc[40, 'cantidad'] = df_banco.loc[40, 'cantidad'] * 10
df_banco.loc[40, 'monto_total'] = round(df_banco.loc[40, 'cantidad'] * df_banco.loc[40, 'precio_unitario'], 2)

# Error 3: Diferencia de centavos
df_banco.loc[75, 'monto_total'] = df_banco.loc[75, 'monto_total'] - 1500.50

# GUARDAR COMO EXCEL REAL
df_banco.to_excel('registro_interno_banco.xlsx', index=False)

print("¡Archivos base guardados correctamente en formato Excel (.xlsx) con columnas separadas!")