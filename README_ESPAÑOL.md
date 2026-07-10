# conciliacion-automatizada-backoffice
Automatización de procesos de conciliación diaria y control de riesgos operativos en Back Office mediante Python, SQL y Power BI.
# 📊 Automatización de Conciliación Diaria y Control de Riesgo Operativo (Back Office)

## 📌 Contexto del Proyecto
En el día a día de un Back Office de Tesorería o Liquidaciones en una entidad financiera, el volumen de operaciones procesadas en mercados como **BYMA** (Bolsas y Mercados Argentinos) y **MAV** (Mercado Argentino de Valores) hace inviable y riesgoso el control manual fila por fila. Un error de tipeo en la carga interna puede generar severos desajustes de caja en el día de liquidación ($T+1$ / $T+2$).

Este proyecto desarrolla un **pipeline automatizado de datos** que extrae la información de mercado, la cruza con los registros internos de la Mesa de Operaciones del banco mediante **Python (Pandas)**, almacena y audita la información en una base de datos relacional **SQL (SQLite)**, y genera un reporte automatizado de excepciones para mitigar riesgos operativos.

---

## 🛠️ Tecnologías Utilizadas
* **Python:** Extracción de datos, simulación de la rueda y motor de conciliación automatizada con la librería `Pandas`.
* **SQL (SQLite):** Estructuración de datos financieros en un motor relacional y auditoría mediante consultas complejas (`LEFT JOIN` e `INNER JOIN`).
* **Excel (OpenPyXL):** Generación automática del entregable diario con casillas independientes para el equipo de Liquidaciones.

---

## 🔍 Arquitectura del Pipeline de Control

El proceso sigue un flujo estructurado de datos para garantizar el control de la rueda:
1. **Extracción:** Se absorben los reportes del mercado externo e interno (`.xlsx`).
2. **Ingeniería/Conversión:** Python convierte las planillas en tablas de base de datos SQL relacionales.
3. **Auditoría Financiera:** Se ejecutan consultas SQL específicas para detectar anomalías de manera instantánea.

---

## 🚨 Reporte de Hallazgos y Análisis de Riesgo (Caso Práctico)

Tras procesar una rueda simulada de 100 operaciones con activos reales del mercado local (como los bonos soberanos `AL30`, `GD30` y la acción de `PAMP`), el sistema detectó con éxito **3 anomalías críticas** clasificadas en dos categorías:

### 1. Fugas de Información (Operaciones Omitidas)
* **Boleto Detectado:** `500016` (Especie: `PAMP`).
* **Impacto:** El mercado liquidó una operación por **$3.109.591,67** que la mesa del banco omitió por completo cargar en el sistema interno. 
* **Riesgo mitigado:** Evita un pasivo no contabilizado oculto de cara al cierre de saldos.

### 2. Descuadres Numéricos de Caja
El cruce relacional detectó diferencias en los montos de operaciones registradas en ambos sistemas:

| ID Boleto | Activo | Cantidad BYMA | Cantidad Banco | Monto BYMA | Monto Banco | Diferencia Económica | Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **500076** | GD30 | 100 | 100 | $6.485.213,99 | $6.483.713,49 | **$1.500,50** | Desfasaje típico por redondeo analítico de tasas/comisiones. |
| **500041** | PAMP | 1.000 | 10.000 | $3.133.306,24 | $31.333.100,00 | **-$28.199.793,76** | **Anomalía Crítica:** Error humano de carga en el teclado de la Mesa (se agregó un cero de más en la cantidad). |

> 💡 **Impacto del Analista:** La alerta temprana sobre el boleto `500041` frenó un descuadre ficticio de caja de **28 millones de pesos** antes de la apertura del mercado del día siguiente, previniendo penalizaciones de la cámara compensadora y problemas de liquidez.

---

## 📂 Cómo Ejecutar el Proyecto
1. Clonar el repositorio.
2. Ejecutar `python generar_datos.py` para simular las planillas de la rueda financiera.
3. Ejecutar `python migrar_a_sql.py` para inyectar los datos en el motor relacional.
4. Ejecutar `python conciliacion_diaria.py` para auditar el cierre del día y generar el archivo `reporte_excepciones_diarias.xlsx`.
