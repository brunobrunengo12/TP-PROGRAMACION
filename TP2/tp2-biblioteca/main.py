from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables

from models.autor import Autor  # noqa: F401
from models.libro import Libro  # noqa: F401
from models.libro_autor import LibroAutor  # noqa: F401
from models.socio import Socio  # noqa: F401
from models.prestamo import Prestamo  # noqa: F401
from routers import autor, libro, socio


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="API Biblioteca", lifespan=lifespan)

app.include_router(autor.router)
app.include_router(libro.router)
app.include_router(socio.router)


@app.get("/")
async def root():
    return {"message": "API Biblioteca"}