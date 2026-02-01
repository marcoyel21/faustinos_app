SUMMARY_QUERY = """
SELECT
    s.id,
    COUNT(*) AS partidos_jugados,
    SUM(s.cambio) AS cambios,
    SUM(s.gol) AS goles,
    SUM(s.asistencia) AS asistencias,
    COALESCE(m.total_aportaciones, 0) AS arbitrajes
FROM stats s
LEFT JOIN (
    SELECT id, SUM(cantidad) AS total_aportaciones
    FROM money
    GROUP BY id
) m ON s.id = m.id
GROUP BY s.id;
"""