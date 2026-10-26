
import os
import time
import logging
from typing import List
import sentry_sdk

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError


# CONFIGURACION DE LOGS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CONFIGURACION DE BASE DE DATOS

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")
DB_NAME = os.getenv("DB_NAME", "tienda")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

DB_SSL = os.getenv("DB_SSL", "false").lower() == "true"

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = URL.create(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )

# Aiven requiere conexion SSL.
# En Docker local no es obligatorio.
connect_args = {}

if DB_SSL:
    connect_args = {
        "ssl": {
            "ssl_mode": "REQUIRED"
        }
    }

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=280,
    connect_args=connect_args,
)

# VERIFICAR CONEXIÓN A MYSQL

def verificar_conexion():
    for intento in range(10):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            logger.info("Conectado correctamente a MySQL")
            return

        except SQLAlchemyError as error:
            logger.warning(
                "Esperando base de datos. Intento %s/10: %s",
                intento + 1,
                type(error).__name__
            )
            time.sleep(3)

    logger.warning(
        "No se pudo conectar a MySQL durante el inicio."
    )


verificar_conexion()

# CONFIGURACIÓN DE SENTRY

if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        environment=os.getenv("ENVIRONMENT", "development"),
        traces_sample_rate=0.1,
        enable_logs=True,
        send_default_pii=False,
    )

# INICIALIZACIÓN DE FASTAPI

app = FastAPI(
    title="API Actividad 7",
    description="Backend FastAPI con despliegue continuo",
    version="1.0.0"
)


# CONFIGURACIÓN CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)



# MODELOS

class Usuario(BaseModel):
    id: int
    nombre: str
    email: str


# ENDPOINT PRINCIPAL


@app.get("/")
def estado():
    return {
        "mensaje": "API Actividad 7 funcionando",
        "estado": "online"
    }



@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "backend-actividad7",
        "environment": os.getenv(
            "ENVIRONMENT",
            "development"
        )
    }


@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    try:
        with engine.connect() as conn:
            filas = conn.execute(
                text(
                    "SELECT id, nombre, email "
                    "FROM usuarios ORDER BY id"
                )
            ).mappings().all()

        return [dict(fila) for fila in filas]

    except SQLAlchemyError:
        logger.exception("Error al consultar usuarios")
        raise HTTPException(
            status_code=503,
            detail="Error de conexión con la base de datos"
        )


# ==========================================
# OBTENER USUARIO POR ID
# ==========================================

@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int):
    try:
        with engine.connect() as conn:
            fila = conn.execute(
                text(
                    "SELECT id, nombre, email "
                    "FROM usuarios WHERE id = :id"
                ),
                {"id": usuario_id},
            ).mappings().first()

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return dict(fila)

    except SQLAlchemyError:
        logger.exception(
            "Error al consultar usuario %s",
            usuario_id
        )
        raise HTTPException(
            status_code=503,
            detail="Error de conexión con la base de datos"
        )

@app.get("/test-sentry")
def test_sentry():
    if os.getenv("ENABLE_SENTRY_TEST", "false").lower() != "true":
        raise HTTPException(
            status_code=404,
            detail="Not Found"
        )

    division_por_cero = 1 / 0
    return {"resultado": division_por_cero}