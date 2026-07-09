import pandas as pd
import sqlite3

# Paso 1: Crear y conectarse a la base de datos SQL (se genera un archivo llamado banco.db)
conexion = sqlite3.connect('banco.db')

# Paso 2: Leer los archivos Excel independientes que creamos antes
df_byma = pd.read_excel('operaciones_byma.xlsx')
df_banco = pd.read_excel('registro_interno_banco.xlsx')

# Paso 3: Volcar los datos en tablas SQL
# 'to_sql' agarra el Excel y lo transforma en una tabla estructurada adentro de la base de datos
df_byma.to_sql('operaciones_byma', conexion, if_exists='replace', index=False)
df_banco.to_sql('registro_interno_banco', conexion, if_exists='replace', index=False)

print("¡Éxito! Las planillas de Excel ahora son tablas reales dentro de la base de datos SQL 'banco.db'.")

# Cerramos la conexión por seguridad
conexion.close()