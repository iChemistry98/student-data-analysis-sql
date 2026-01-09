import re
import pandas as pd
import mysql.connector

csv_path = r"C:\Users\Lenovo\Documents\UPWORK\Portafolio\student_data_cleaning\data\students_clean.csv"
df = pd.read_csv(csv_path, encoding="latin1")

# Selección por POSICIÓN (según tu header real)
# 0 marca_temporal
# 1 edad
# 2 sexo
# 3 semestre (ej. "7mo", "11vo")
# 4 trabaja
# 5 apoyo_economico
# 6 impacto_economico
# ...
# 22 motivacion
# 25 seguridad_futuro
df = df.iloc[:, [1, 2, 3, 4, 5, 6, 22, 25]].copy()
df.columns = [
    "edad",
    "sexo",
    "semestre",
    "trabaja",
    "apoyo_economico",
    "impacto_economico",
    "motivacion",
    "seguridad_futuro",
]

# --- Limpieza mínima robusta ---

def extract_int(x):
    """Extrae el primer número de un texto tipo '7mo', '11vo'. Si no hay, regresa None."""
    if pd.isna(x):
        return None
    m = re.search(r"\d+", str(x))
    return int(m.group()) if m else None

# semestre -> int
df["semestre"] = df["semestre"].apply(extract_int)

# edad -> int (si se puede)
df["edad"] = pd.to_numeric(df["edad"], errors="coerce").apply(lambda v: int(v) if pd.notna(v) else None)

# escalas -> int (si se puede)
for c in ["impacto_economico", "motivacion", "seguridad_futuro"]:
    df[c] = pd.to_numeric(df[c], errors="coerce").apply(lambda v: int(v) if pd.notna(v) else None)

# texto limpio
for c in ["sexo", "trabaja", "apoyo_economico"]:
    df[c] = df[c].astype(str).str.strip()
    # si quedó "nan" por conversión a string, lo regresamos a None
    df[c] = df[c].replace({"nan": None, "None": None, "": None})

# IMPORTANTÍSIMO: convierte cualquier NA de pandas a None (MySQL sí acepta None)
df = df.where(pd.notna(df), None)

# --- Conexión e inserción ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="student_analysis_db",
)
cursor = conn.cursor()

insert_sql = """
INSERT INTO students
(edad, sexo, semestre, trabaja, apoyo_economico, impacto_economico, motivacion, seguridad_futuro)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

rows = [tuple(r) for r in df.to_numpy()]
cursor.executemany(insert_sql, rows)

conn.commit()
cursor.close()
conn.close()

print(f"✅ Insertadas {len(rows)} filas en MySQL")
