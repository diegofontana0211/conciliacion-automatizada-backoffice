-- ==============================================================================
-- QUERY 1: DETECCIÓN DE FUGAS DE INFORMACIÓN (OPERACIONES OMIDITAS POR EL BANCO)
-- Lógica: Buscamos boletos liquidados en mercado (BYMA) que no impactaron en el banco.
-- ==============================================================================
SELECT 
    byma.id_boleto,
    byma.especie,
    byma.cantidad,
    byma.monto_total AS monto_byma
FROM operaciones_byma AS byma
LEFT JOIN registro_interno_banco AS banco 
    ON byma.id_boleto = banco.id_boleto
WHERE banco.id_boleto IS NULL;

-- RESULTADO DEL CONTROL:
-- Se detectó que el id_boleto 500016 (Especie: PAMP) por un monto de $3.109.591,67 
-- fue omitido en el registro interno del banco. Riesgo de pasivo no contabilizado.

-- ==============================================================================
-- QUERY 2: DETECCIÓN DE DESCUADRES NUMÉRICOS (ERRORES DE LIQUIDACIÓN Y CARGA)
-- Lógica: Cruzamos registros existentes en ambos lados cuyos montos totales difieran.
-- ==============================================================================
SELECT 
    byma.id_boleto,
    byma.especie AS especie_byma,
    byma.cantidad AS cant_byma,
    banco.cantidad AS cant_banco,
    byma.monto_total AS monto_byma,
    banco.monto_total AS monto_banco,
    (byma.monto_total - banco.monto_total) AS diferencia_monto
FROM operaciones_byma AS byma
INNER JOIN registro_interno_banco AS banco 
    ON byma.id_boleto = banco.id_boleto
WHERE (byma.monto_total - banco.monto_total) <> 0;

-- RESULTADOS DEL CONTROL:
-- 1. id_boleto 500076 (Especie: GD30): Diferencia menor de $1.500,50 (Desfasaje típico por redondeo de tasas/comisiones).
-- 2. id_boleto 500041 (Especie: PAMP): Anomalía crítica de -$28.199.793,76 causada por error humano de carga 
--    en la Mesa de Operaciones (se ingresaron 10.000 nominales en el sistema interno en lugar de los 1.000 reales de BYMA). 
--    Esta alerta temprana previene un descuadre de caja severo al momento de la liquidación forzosa.
