# Actividad 7 — Despliegue continuo y observabilidad

Es una aplicacion web que muestra un saludo personalizado y una lista de usuarios guardados en MySQL. El frontend consulta una API FastAPI y muestra los datos recibidos.

El proyecto parte de la **Actividad 2** y fue adaptado para funcionar en la nube, con despliegue automático y monitoreo de errores.

**Integrantes:** Tiago Robles, Joaquín Paramo, Juan Pablo Mora y Rodrigo.

## Tecnologías utilizadas

- **Frontend:** HTML, CSS y JavaScript, publicado en **Netlify**.
- **Backend:** Python y **FastAPI**, ejecutado con **Docker** en **Render**.
- **Base de datos:** **MySQL** alojada en **Aiven**, conectada mediante SQLAlchemy y PyMySQL.
- **Repositorio y despliegues:** GitHub (`main`), conectado a Netlify y Render.
- **Observabilidad:** **Sentry** para registrar errores y ver su stack trace.

## Enlaces para probar el funcionamiento

- **Web:** https://prismatic-kangaroo-67af2c.netlify.app
- **API:** https://gestion-desarrollo-actividad7-api.onrender.com
- **Documentación de FastAPI:** https://gestion-desarrollo-actividad7-api.onrender.com/docs
- **Usuarios:** https://gestion-desarrollo-actividad7-api.onrender.com/usuarios
- **Estado del backend:** https://gestion-desarrollo-actividad7-api.onrender.com/health
- **Sentry (requiere acceso):** https://gestion-desarrollo-actividad7.sentry.io


## Pruebas de la app

1. Abrir la **web de Netlify**. Debe aparecer el saludo **«¡Bienvenido/a, Tiago!»** y la lista de los cuatro integrantes.
2. Presionar **Recargar**: la página vuelve a consultar la API y muestra los usuarios de MySQL.
3. Abrir **`/usuarios`** en Render: debe devolver los usuarios en formato JSON.
4. Abrir **`/health`**: debe devolver `"status": "ok"`, `"environment": "production"` y la versión `"1.1.0"`.
5. Entrar a **`/docs`** para consultar y probar los endpoints desde Swagger.

## Cómo comprobar el correcto despliegue automático

El frontend y el backend están conectados a la rama `main` de este repositorio.

1. Modificar un texto de `frontend/index.html`, hacer commit y ejecutar `git push origin main`.
2. Revisar **Deploys** en Netlify: debe generarse un despliegue automático y reflejarse el cambio en la web.
3. Modificar la respuesta de `/health` en `backend/main.py`, hacer commit y ejecutar `git push origin main`.
4. Revisar **Deploys** en Render: debe aparecer un despliegue con el origen **Auto-Deploy**. Al finalizar, consultar `/health` para ver el cambio.

Estas pruebas ya las realizamos: Netlify publicó el cambio de titulo y Render publicó la versión `1.1.0` del backend.

## Cómo comprobar Sentry

Se integró Sentry en FastAPI y se realizó una prueba con el endpoint `/test-sentry`. El panel registró una excepción **`ZeroDivisionError`**, mostrando el archivo `main.py`, la función `test_sentry` y la línea que produjo el error.

Para revisar esto, ingresar al panel de **Sentry → Issues** con una cuenta autorizada y abrir el evento registrado.

## Ejecución local (opcional)

El proyecto conserva la configuración Docker Compose de la Actividad 2. Para levantarla localmente:

1. Tener Docker Desktop abierto.
2. Crear `.env` a partir de `.env.example` y completar las variables requeridas.
3. Ejecutar:

```bash
docker compose up --build
```

**Nota:** `frontend/app.js` apunta actualmente al backend de Render. Para probar todo de manera local, cambiar esa URL por la dirección del backend local.

Para detener los contenedores:

```bash
docker compose down
```
