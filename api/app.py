import os
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

def conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )

# ---------- GET ----------
@app.get("/resultados")
def get_all():
    with conn() as c, c.cursor() as cur:
        cur.execute("SELECT producto, ingreso FROM resultados ORDER BY ingreso DESC;")
        return [{"producto": p, "ingreso": float(i)} for p, i in cur.fetchall()]

@app.get("/resultados/{producto}")
def get_one(producto: str):
    with conn() as c, c.cursor() as cur:
        cur.execute("SELECT producto, ingreso FROM resultados WHERE producto = %s;", (producto,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(404, "Producto no encontrado")
        return {"producto": row[0], "ingreso": float(row[1])}

# ---------- POST ----------
class Resultado(BaseModel):
    producto: str
    ingreso: float

@app.post("/resultados")
def crear(r: Resultado):
    with conn() as c, c.cursor() as cur:
        cur.execute("""
            INSERT INTO resultados (producto, ingreso) VALUES (%s, %s)
            ON CONFLICT (producto) DO UPDATE SET ingreso = EXCLUDED.ingreso;
        """, (r.producto, r.ingreso))
        c.commit()
    return {"ok": True, "producto": r.producto}

# ---------- DELETE ----------
@app.delete("/resultados/{producto}")
def borrar(producto: str):
    with conn() as c, c.cursor() as cur:
        cur.execute("DELETE FROM resultados WHERE producto = %s;", (producto,))
        if cur.rowcount == 0:
            raise HTTPException(404, "No existe")
        c.commit()
    return {"ok": True}