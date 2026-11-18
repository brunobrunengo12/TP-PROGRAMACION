# Clase FastAPI

Clase para aprender **FastAPI** y **Pydantic**.

## Crear el entorno virtual (venv)

Desde esta carpeta (`clase-fastapi`):

```bash
python3 -m venv .venv
```

Activar el entorno virtual:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

## Instalar los requerimientos

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

## Ejecutar la aplicaciÃ³n

```bash
fastapi dev main.py
```

La API quedarÃ¡ disponible en `http://127.0.0.1:8000` y la documentaciÃ³n interactiva en `http://127.0.0.1:8000/docs`.

## Lint y chequeo de tipos

El proyecto incluye configuraciÃ³n local para dos herramientas:

- **[`setup.cfg`](./setup.cfg)**: configuraciÃ³n de [`pycodestyle`](https://pycodestyle.pycqa.org/) (chequeo de estilo PEP 8). Define `max-line-length = 79` y excluye `.venv` y `__pycache__` del anÃ¡lisis.
- **[`pyrightconfig.json`](./pyrightconfig.json)**: configuraciÃ³n de [`pyright`](https://microsoft.github.io/pyright/) (chequeo de tipos). Apunta al entorno virtual local (`.venv`) para resolver las dependencias instaladas y excluye `.venv` y `__pycache__`.

`pyright` ya estÃ¡ incluido en `requirements.txt`. `pycodestyle` no, asÃ­ que hay que instalarlo aparte.

Con el entorno virtual activado, correr:

```bash
pip install pycodestyle
python -m pycodestyle .
```

```bash
pyright
```


---

# TP2 - Sistema de Biblioteca (FastAPI + SQLModel)

API REST para gestionar el catÃ¡logo de una biblioteca (autores, libros y socios) y sus prÃ©stamos.

## Estructura

```text
tp2-biblioteca/
â”œâ”€â”€ main.py            # crea la app y registra los routers
â”œâ”€â”€ database.py        # conexiÃ³n SQLite, creaciÃ³n de tablas y sesiÃ³n (SessionDep)
â”œâ”€â”€ models/            # tablas SQLModel y esquemas: Autor, Libro, LibroAutor, Socio, Prestamo
â”œâ”€â”€ routers/           # endpoints: solo traducen HTTP, no tienen reglas
â”œâ”€â”€ services/          # reglas de negocio (las 8 del enunciado) y consultas a la base
â”œâ”€â”€ tests/             # pytest con base en memoria
â””â”€â”€ requirements.txt   # dependencias del proyecto
```

Cada pedido recorre las capas asÃ­: **router â†’ service â†’ base de datos**.
- El **router** recibe el pedido HTTP y devuelve la respuesta.
- El **service** aplica las reglas de negocio, consulta la base de datos y decide los errores (`404`, `403`, `409`).

## CÃ³mo correrlo

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

La API queda en `http://127.0.0.1:8000` y la documentaciÃ³n interactiva en `http://127.0.0.1:8000/docs`. La base de datos (`biblioteca.db`) se crea sola la primera vez.
Si se hacen cambios en los campos de algÃºn modelo, hay que borrar `biblioteca.db` para que se cree de nuevo con las columnas nuevas.

## CÃ³mo testear

```powershell
pytest
```

Con cobertura:

```powershell
pytest --cov=. --cov-report=term-missing
```

Los tests usan una base de datos SQLite en memoria, asÃ­ que no tocan `biblioteca.db`.

## Endpoints

| MÃ©todo | Ruta | DescripciÃ³n |
|---|---|---|
| POST / GET / PUT / DELETE | `/autores` | Alta, consulta (soporta `?offset=&limit=`), modificaciÃ³n y baja de autores |
| POST / GET / PUT / DELETE | `/libros` | Ãdem para libros (la respuesta incluye sus autores; soporta `?offset=&limit=`) |
| POST / GET / PUT / DELETE | `/socios` | Ãdem para socios (soporta `?offset=&limit=`) |
| POST | `/libros/{id}/autores/{autor_id}` | Asocia un autor a un libro |
| GET | `/libros?disponibles=true` | Libros con `stock > 0` (combinable con `offset` y `limit`) |
| POST | `/prestamos` | Registra un prÃ©stamo (`socio_id`, `libro_id`) |
| POST | `/prestamos/{id}/devolucion` | Registra la devoluciÃ³n |
| GET | `/socios/{id}/prestamos?activos=true` | PrÃ©stamos activos del socio |

## Reglas de negocio

| # | Regla | Error |
|---|---|---|
| 1 | Un socio no puede tener mÃ¡s de 3 prÃ©stamos activos | 409 |
| 2 | No se presta un libro sin stock; al prestar se descuenta 1 | 409 |
| 3 | Un socio inactivo no puede pedir prÃ©stamos | 403 |
| 4 | El plazo es de 14 dÃ­as (`fecha_vencimiento = fecha_prestamo + 14 dÃ­as`) | n/a |
| 5 | Al devolver se repone el stock y se calcula la multa: $100 por dÃ­a de atraso (0 si llegÃ³ a tiempo) | n/a |
| 6 | No se puede devolver un prÃ©stamo ya devuelto | 409 |
| 7 | Recurso inexistente | 404 |
| 8 | ISBN o email duplicado | 409 |

AdemÃ¡s de las reglas del enunciado:
- El stock negativo se rechaza con `422`.
- Los emails con formato invÃ¡lido en socios se rechazan con `422` (`EmailStr`).
- La paginaciÃ³n en `GET /autores`, `GET /libros` y `GET /socios` acepta `offset >= 0` (por defecto 0) y `1 <= limit <= 100` (por defecto 100), rechazando valores fuera de rango con `422`.
- No se puede borrar un libro ni un socio que tenga prÃ©stamos registrados (`409`).
