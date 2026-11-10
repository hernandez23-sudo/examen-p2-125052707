#!/usr/bin/env python3
import os
import psycopg2

# Usamos la ruta que montamos en el docker-compose
CSV_PATH = os.getenv("RESULT_TXT", "/data-output/resultado/part-00000")

# Las variables vienen del .env
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "db"),
    port=os.getenv("DB_PORT", "5432"),
    user=os.getenv("POSTGRES_USER", "datamart"),
    password=os.getenv("POSTGRES_PASSWORD"),
    dbname=os.getenv("POSTGRES_DB", "datamart"),
)

with conn, conn.cursor() as cur:
    # Creamos la tabla si no existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resultados (
            producto TEXT PRIMARY KEY,
            ingreso  DOUBLE PRECISION NOT NULL
        );
    """)
    
    # Leemos el archivo de Hadoop
    with open(CSV_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            producto, ingreso = line.split("\t")
            # Insertamos o actualizamos
            cur.execute("""
                INSERT INTO resultados (producto, ingreso) VALUES (%s, %s)
                ON CONFLICT (producto) DO UPDATE SET ingreso = EXCLUDED.ingreso;
            """, (producto, float(ingreso)))
print("Resultados cargados correctamente.")