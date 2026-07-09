import pandas as pd

def ejecutar_conciliacion():
    print("=== INICIANDO PROCESO DE CONCILIACIÓN DIARIA ===\n")
    
    # 1. Absorber los datos de las planillas del día
    try:
        df_byma = pd.read_csv('operaciones_byma.csv')
        df_banco = pd.read_csv('registro_interno_banco.csv')
    except FileNotFoundError:
        print("Error: No se encontraron los archivos CSV. Corré primero generar_datos.py")
        return

    # 2. ALERTA CRÍTICA: Buscar operaciones del mercado que el banco NO registró (Fugas)
    # Buscamos qué IDs de boleto de BYMA no existen en la planilla interna del banco
    fugas = df_byma[~df_byma['id_boleto'].isin(df_banco['id_boleto'])]
    
    print(f"--> Control de Integridad: Se encontraron {len(fugas)} operaciones omitidas por el banco.")
    if not fugas.empty:
        print(fugas[['id_boleto', 'especie', 'cantidad', 'monto_total']])
    print("-" * 60)

    # 3. CONCILIACIÓN DURÁ: Cruzar las operaciones que sí están en ambos lados para ver si los números coinciden
    # Hacemos un MERGE (un cruce de tablas) usando el 'id_boleto' como llave común
    cruces = pd.merge(df_byma, df_banco, on='id_boleto', suffixes=('_byma', '_banco'))
    
    # Calculamos la diferencia matemática exacta de dinero entre BYMA y nuestro registro
    cruces['diferencia_monto'] = cruces['monto_total_byma'] - cruces['monto_total_banco']
    
    # Filtramos las filas donde la diferencia de plata no sea cero
    descuadres = cruces[cruces['diferencia_monto'] != 0].copy()
    
    print(f"--> Control de Saldos: Se encontraron {len(descuadres)} descuadres numéricos entre registros.")
    
    if not descuadres.empty:
        # Formateamos la salida para que el reporte sea ultra legible
        reporte_descuadres = descuadres[[
            'id_boleto', 'especie_byma', 
            'cantidad_byma', 'cantidad_banco', 
            'monto_total_byma', 'monto_total_banco', 
            'diferencia_monto'
        ]]
        print(reporte_descuadres)
    print("-" * 60)
    
    # 4. EXPORTAR EL REPORTE DE EXCEPCIONES
    if not fugas.empty or not descuadres.empty:
        # Guardamos las alertas en un archivo Excel para mandárselo al equipo de liquidaciones
        with pd.ExcelWriter('reporte_excepciones_diarias.xlsx') as writer:
            if not fugas.empty:
                fugas.to_excel(writer, sheet_name='Operaciones_No_Registradas', index=False)
            if not descuadres.empty:
                reporte_descuadres.to_excel(writer, sheet_name='Diferencias_de_Monto', index=False)
        print("\n[ÉXITO] ¡Se generó el archivo 'reporte_excepciones_diarias.xlsx' con las anomalías!")
    else:
        print("\n[OK] Rueda perfecta. No se detectaron anomalías.")

if __name__ == "__main__":
    ejecutar_conciliacion()