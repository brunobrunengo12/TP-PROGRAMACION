# TP1 - API REST con FastAPI (Usuarios y Libros)

API REST desarrollada con FastAPI y Pydantic como extensión de la primera clase práctica. Gestiona dos recursos en memoria: usuarios (`/user`) y libros (`/libro`), con soporte para operaciones CRUD, filtros por parámetros de consulta y manejo de errores HTTP.

## Estructura

```text
TP1/
└── clase-fastapi/
    ├── main.py              # instancia la app de FastAPI y registra los routers
    ├── models/              # modelos Pydantic de entrada y esquemas de respuesta
    │   ├── users.py
    │   └── libros.py
    ├── routers/             # endpoints y lógica de manejo en memoria
    │   ├── users.py
    │   └── libros.py
    └── requirements.txt     # dependencias del proyecto
```

## Cómo correrlo

Todos los comandos se ejecutan desde la carpeta `TP1/clase-fastapi`.

Crear y activar el entorno virtual:

```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

Levantar el servidor de desarrollo:

```powershell
fastapi dev main.py
```

La API queda disponible en `http://127.0.0.1:8000` y la documentación interactiva (Swagger UI) en `http://127.0.0.1:8000/docs`.

## Endpoints

### Usuarios (`/user`)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/user` | Lista todos los usuarios. Acepta filtro opcional `?is_active=true` o `?is_active=false` |
| POST | `/user` | Crea un nuevo usuario (`id`, `name`, `is_active` opcional con valor `true` por defecto) |
| PUT | `/user/{id}` | Actualiza los datos de un usuario existente manteniendo su `id` (404 si no existe) |
| DELETE | `/user/{id}` | Elimina un usuario por su `id` (404 si no existe) |

### Libros (`/libro`)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/libro` | Lista todos los libros. Acepta filtro opcional `?autor=<nombre>` |
| GET | `/libro/{id}` | Obtiene un libro por su `id` (404 si no existe) |
| POST | `/libro` | Crea un nuevo libro (`id`, `titulo`, `autor`, `isbn`, `anio`) |
| PUT | `/libro/{id}` | Actualiza un libro existente manteniendo su `id` (404 si no existe) |
| DELETE | `/libro/{id}` | Elimina un libro por su `id` (404 si no existe) |