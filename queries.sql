-- Student Data Analysis Queries (MySQL)
USE student_analysis_db;

-- 1) Distribución por semestre
SELECT
  semestre,
  COUNT(*) AS total_estudiantes
FROM students
GROUP BY semestre
ORDER BY semestre;

-- 2) Promedio de motivación y seguridad futura por semestre
SELECT
  semestre,
  ROUND(AVG(motivacion), 2) AS prom_motivacion,
  ROUND(AVG(seguridad_futuro), 2) AS prom_seguridad_futuro
FROM students
GROUP BY semestre
ORDER BY semestre;

-- 3) ¿Cuántos trabajan? (conteo y porcentaje)
SELECT
  trabaja,
  COUNT(*) AS total,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM students), 2) AS porcentaje
FROM students
GROUP BY trabaja
ORDER BY total DESC;

-- 4) Impacto económico (escala) vs promedio de motivación
SELECT
  impacto_economico,
  COUNT(*) AS total,
  ROUND(AVG(motivacion), 2) AS prom_motivacion
FROM students
GROUP BY impacto_economico
ORDER BY impacto_economico;

-- 5) Apoyo económico más común (Top 5)
SELECT
  apoyo_economico,
  COUNT(*) AS total
FROM students
GROUP BY apoyo_economico
ORDER BY total DESC
LIMIT 5;

-- 6) Segmentación de "riesgo" (ejemplo simple con CASE)
-- Criterio: alta afectación económica (>=4) y baja motivación (<=2)
SELECT
  CASE
    WHEN impacto_economico >= 4 AND motivacion <= 2 THEN 'Riesgo alto'
    WHEN impacto_economico >= 3 AND motivacion <= 3 THEN 'Riesgo medio'
    ELSE 'Riesgo bajo'
  END AS nivel_riesgo,
  COUNT(*) AS total
FROM students
GROUP BY nivel_riesgo
ORDER BY total DESC;

-- 7) Perfil de riesgo por semestre (para ver dónde se concentra)
SELECT
  semestre,
  SUM(CASE WHEN impacto_economico >= 4 AND motivacion <= 2 THEN 1 ELSE 0 END) AS riesgo_alto,
  COUNT(*) AS total,
  ROUND(
    SUM(CASE WHEN impacto_economico >= 4 AND motivacion <= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
    2
  ) AS porcentaje_riesgo_alto
FROM students
GROUP BY semestre
ORDER BY semestre;
