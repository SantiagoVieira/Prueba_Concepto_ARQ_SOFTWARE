"""
Prueba de concepto: Backend (API de tareas)
Arquitectura de Software - Universidad de Medellín

Demuestra: capas separadas, validación de entradas, autenticación con token,
persistencia en base de datos (SQLite) y documentación automática (OpenAPI).
"""
import sqlite3

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="PoC Backend: API de tareas", version="1.0")
DB = "tareas.db"
API_TOKEN = "demo-token"  # En producción: JWT/OAuth y secretos en variables de entorno


# ---------- Capa de datos ----------
def conexion():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute(
        "CREATE TABLE IF NOT EXISTS tareas ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "titulo TEXT NOT NULL, hecha INTEGER NOT NULL DEFAULT 0)"
    )
    return con


# ---------- Modelos (validación de entrada y salida) ----------
class TareaIn(BaseModel):
    titulo: str = Field(min_length=3, max_length=100)


class TareaOut(BaseModel):
    id: int
    titulo: str
    hecha: bool


# ---------- Seguridad ----------
def autenticar(authorization: str = Header(default="")):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Token inválido o ausente")


# ---------- Capa de servicio / endpoints ----------
@app.get("/salud")
def salud():
    return {"estado": "ok"}  # Health check para balanceadores y monitoreo


@app.post("/v1/tareas", response_model=TareaOut, status_code=201,
          dependencies=[Depends(autenticar)])
def crear(tarea: TareaIn):
    with conexion() as con:
        cur = con.execute("INSERT INTO tareas (titulo) VALUES (?)", (tarea.titulo,))
        return TareaOut(id=cur.lastrowid, titulo=tarea.titulo, hecha=False)


@app.get("/v1/tareas", response_model=list[TareaOut],
         dependencies=[Depends(autenticar)])
def listar(limite: int = 20):
    with conexion() as con:
        filas = con.execute("SELECT * FROM tareas LIMIT ?", (min(limite, 100),)).fetchall()
        return [TareaOut(id=f["id"], titulo=f["titulo"], hecha=bool(f["hecha"])) for f in filas]


@app.patch("/v1/tareas/{tarea_id}/completar", response_model=TareaOut,
           dependencies=[Depends(autenticar)])
def completar(tarea_id: int):
    with conexion() as con:
        cur = con.execute("UPDATE tareas SET hecha = 1 WHERE id = ?", (tarea_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        f = con.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,)).fetchone()
        return TareaOut(id=f["id"], titulo=f["titulo"], hecha=bool(f["hecha"]))
