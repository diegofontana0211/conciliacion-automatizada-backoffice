import pandas as pd

def ejecutar_conciliacion():
    print("=== INICIANDO PROCESO DE CONCILIACIÓN DIARIA ===\n")
    
    # 1. Absorber los datos directamente desde las planillas Excel (.xlsx)
    try:
        df_byma = pd.read_excel('operaciones_byma.xlsx')
        df_banco = pd.read_excel('registro_interno_banco.xlsx')
    except FileNotFoundError:
        print("Error: No se encontraron los archivos Excel. Corré primero generar_datos.py")
        return

    # 2. ALERTA CRÍTICA: Buscar operaciones del mercado que el banco NO registró (Fugas)
    fugas = df_byma[~df_byma['id_boleto'].isin(df_banco['id_boleto'])]
    
    print(f"--> Control de Integridad: Se encontraron {len(fugas)} operaciones omitidas por el banco.")
    if not fugas.empty:
        print(fugas[['id_boleto', 'especie', 'cantidad', 'monto_total']])
    print("-" * 60)

    # 3. CONCILIACIÓN DURA: Cruzar registros para ver si los números coinciden
    cruces = pd.merge(df_byma, df_banco, on='id_boleto', suffixes=('_byma', '_banco'))
    cruces['diferencia_monto'] = cruces['monto_total_byma'] - cruces['monto_total_banco']
    
    descuadres = cruces[cruces['diferencia_monto'] != 0].copy()
    
    print(f"--> Control de Saldos: Se encontraron {len(descuadres)} descuadres numéricos.")
    
    if not descuadres.empty:
        reporte_descuadres = descuadres[[
            'id_boleto', 'especie_byma', 
            'cantidad_byma', 'cantidad_banco', 
            'monto_total_byma', 'monto_total_banco', 
            'diferencia_monto'
        ]]
        print(reporte_descuadres)
    print("-" * 60)
    
    # 4. EXPORTAR EL REPORTE DE EXCEPCIONES EN CASILLAS SEPARADAS
    if not fugas.empty or not descuadres.empty:
        with pd.ExcelWriter('reporte_excepciones_diarias.xlsx', engine='openpyxl') as writer:
            if not fugas.empty:
                reporte_fugas = fugas[['id_boleto', 'especie', 'cantidad', 'precio_unitario', 'monto_total']]
                reporte_fugas.to_excel(writer, sheet_name='Operaciones_No_Registradas', index=False)
            if not descuadres.empty:
                reporte_descuadres.to_excel(writer, sheet_name='Diferencias_de_Monto', index=False)
        print("\n[ÉXITO] ¡Se generó el archivo 'reporte_excepciones_diarias.xlsx' en columnas limpias!")
    else:
        print("\n[OK] Rueda perfecta. No se detectaron anomalías.")

if __name__ == "__main__":
    ejecutar_conciliacion()
