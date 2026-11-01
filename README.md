# Prueba de concepto: Backend (API de tareas)

Arquitectura de Software, Universidad de Medellín.
Componente analizado: **Backend**. Demuestra capas separadas, validación de entradas,
autenticación con token, persistencia en SQLite y documentación automática (OpenAPI).

## Requisitos
- Python 3.10 o superior
- Visual Studio Code con la extensión **Python** (y opcionalmente **REST Client**)

## Puesta en marcha en VS Code (Windows / PowerShell)

1. Abre la carpeta `Prueba_Concepto_ARQ_SOFTWARE` en VS Code (Archivo > Abrir carpeta).
2. Abre una terminal (Ctrl + ñ) y crea el entorno virtual:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> Si PowerShell bloquea el script de activación, ejecuta una sola vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

3. Selecciona el intérprete: Ctrl + Shift + P > *Python: Select Interpreter* > `.venv`.
4. Enciende el servidor (opción A o B):
   - **A.** Terminal: `uvicorn main:app --reload`
   - **B.** Pulsa **F5** (configuración "Backend: FastAPI (uvicorn)").
5. Abre en el navegador: <http://127.0.0.1:8000/docs> (Swagger UI interactivo).
   En **Authorize** / cada endpoint usa el encabezado `Authorization: Bearer demo-token`.

## Probar la API
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **REST Client:** abre `requests.http` y pulsa *Send Request* sobre cada bloque.
- **PowerShell:** con el servidor encendido, en otra terminal: `.\demo.ps1`

## Pruebas automáticas
```powershell
python -m pytest -q
```
Deben pasar las 5 pruebas (salud, sin token, validación, flujo completo y 404).

## Endpoints
| Método | Ruta | Descripción | Respuestas |
|---|---|---|---|
| GET | `/salud` | Health check | 200 |
| POST | `/v1/tareas` | Crear tarea | 201, 401, 422 |
| GET | `/v1/tareas?limite=20` | Listar tareas (máx. 100) | 200, 401 |
| PATCH | `/v1/tareas/{id}/completar` | Marcar como hecha | 200, 401, 404 |

## Qué demuestra
| Concepto | Dónde se ve |
|---|---|
| Separación de responsabilidades | `main.py`: datos, modelos, seguridad y endpoints separados |
| Validación de entrada | `TareaIn` rechaza títulos < 3 o > 100 caracteres (422) |
| Autenticación | `autenticar` devuelve 401 sin token |
| Códigos HTTP correctos | 201 al crear, 404 si no existe, 401 sin permiso |
| Consultas parametrizadas | Los `?` evitan inyección SQL |
| Límite en listados | `min(limite, 100)` |
| Versionado y salud | Ruta `/v1/` y `/salud` |
| Documentación automática | `/docs` generada desde el contrato |

## Siguientes pasos hacia producción
JWT/OAuth en lugar del token fijo, PostgreSQL en lugar de SQLite, caché y rate limiting,
Docker, logs estructurados y pipeline de CI/CD.
