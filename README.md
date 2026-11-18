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

---

# TP2 - Sistema de Biblioteca (FastAPI + SQLModel)

API REST para gestionar el catálogo de una biblioteca (autores, libros y socios) y sus préstamos.

## Estructura

```text
tp2-biblioteca/
├── main.py            # crea la app y registra los routers
├── database.py        # conexión SQLite, creación de tablas y sesión (SessionDep)
├── models/            # tablas SQLModel y esquemas: Autor, Libro, LibroAutor, Socio, Prestamo
├── routers/           # endpoints: solo traducen HTTP, no tienen reglas
├── services/          # reglas de negocio (las 8 del enunciado) y consultas a la base
├── tests/             # pytest con base en memoria
└── requirements.txt   # dependencias del proyecto
```

Cada pedido recorre las capas así: **router → service → base de datos**.
- El **router** recibe el pedido HTTP y devuelve la respuesta.
- El **service** aplica las reglas de negocio, consulta la base de datos y decide los errores (`404`, `403`, `409`).

## Cómo correrlo

Todos los comandos se ejecutan desde la carpeta `TP2/tp2-biblioteca`.

Crear y activar el entorno virtual:

```powershell
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

Levantar la API:

```powershell
fastapi dev main.py
```

La API queda en `http://127.0.0.1:8000` y la documentación interactiva en `http://127.0.0.1:8000/docs`. La base de datos (`biblioteca.db`) se crea sola la primera vez.
Si se hacen cambios en los campos de algún modelo, hay que borrar `biblioteca.db` para que se cree de nuevo con las columnas nuevas.

## Cómo testear

```powershell
pytest
```

Con cobertura:

```powershell
pytest --cov=. --cov-report=term-missing
```

Los tests usan una base de datos SQLite en memoria, así que no tocan `biblioteca.db`.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| POST / GET / PUT / DELETE | `/autores` | Alta, consulta (soporta `?offset=&limit=`), modificación y baja de autores |
| POST / GET / PUT / DELETE | `/libros` | Ídem para libros (la respuesta incluye sus autores; soporta `?offset=&limit=`) |
| POST / GET / PUT / DELETE | `/socios` | Ídem para socios (soporta `?offset=&limit=`) |
| POST | `/libros/{id}/autores/{autor_id}` | Asocia un autor a un libro |
| GET | `/libros?disponibles=true` | Libros con `stock > 0` (combinable con `offset` y `limit`) |
| POST | `/prestamos` | Registra un préstamo (`socio_id`, `libro_id`) |
| POST | `/prestamos/{id}/devolucion` | Registra la devolución |
| GET | `/socios/{id}/prestamos?activos=true` | Préstamos activos del socio |

## Reglas de negocio

| # | Regla | Error |
|---|---|---|
| 1 | Un socio no puede tener más de 3 préstamos activos | 409 |
| 2 | No se presta un libro sin stock; al prestar se descuenta 1 | 409 |
| 3 | Un socio inactivo no puede pedir préstamos | 403 |
| 4 | El plazo es de 14 días (`fecha_vencimiento = fecha_prestamo + 14 días`) | n/a |
| 5 | Al devolver se repone el stock y se calcula la multa: $100 por día de atraso (0 si llegó a tiempo) | n/a |
| 6 | No se puede devolver un préstamo ya devuelto | 409 |
| 7 | Recurso inexistente | 404 |
| 8 | ISBN o email duplicado | 409 |

Además de las reglas del enunciado:
- El stock negativo se rechaza con `422`.
- Los emails con formato inválido en socios se rechazan con `422` (`EmailStr`).
- La paginación en `GET /autores`, `GET /libros` y `GET /socios` acepta `offset >= 0` (por defecto 0) y `1 <= limit <= 100` (por defecto 100), rechazando valores fuera de rango con `422`.
- No se puede borrar un libro ni un socio que tenga préstamos registrados (`409`).
