import os
import time
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text

# Datos de conexión: vienen de las variables del docker-compose
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")
DB_NAME = os.getenv("DB_NAME", "tienda")

from sqlalchemy.engine import URL

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = URL.create(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=3306,
        database=DB_NAME,
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Por las dudas, reintenta hasta que la base responda
for intento in range(10):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Conectado a la base de datos")
        break
    except Exception as error:
        print(f"Esperando a la base... intento {intento + 1}: {error}")
        time.sleep(3)

app = FastAPI(title="API TP Docker")

# CORS: permite que un navegador de otro origen consuma la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic define la forma de los datos que devuelve la API
class Usuario(BaseModel):
    id: int
    nombre: str
    email: str

@app.get("/")
def estado():
    return {"mensaje": "API funcionando"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "backend-actividad7",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    with engine.connect() as conn:
        filas = conn.execute(
            text("SELECT id, nombre, email FROM usuarios ORDER BY id")
        ).mappings().all()
    return [dict(fila) for fila in filas]

@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int):
    with engine.connect() as conn:
        fila = conn.execute(
            text("SELECT id, nombre, email FROM usuarios WHERE id = :id"),
            {"id": usuario_id},
        ).mappings().first()
    if fila is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return dict(fila)
