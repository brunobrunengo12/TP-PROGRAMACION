from typing import Optional
from fastapi import APIRouter, HTTPException, status
from models.libros import (
    Libro,
    UpdateLibroRequest,
    GetLibrosResponse,
    CreateLibroResponse,
    UpdateLibroResponse,
    DeleteLibroResponse,
)

router = APIRouter()

libros_db: list[Libro] = [
    Libro(id=1, titulo="El Aleph", autor="Jorge Luis Borges", isbn="978-9875666481", anio=1949),
    Libro(id=2, titulo="Rayuela", autor="Julio Cortazar", isbn="978-8437624747", anio=1963),
]


@router.get("/libro")
def get_libros(autor: Optional[str] = None) -> GetLibrosResponse:
    if autor is not None:
        filtrados = [l for l in libros_db if autor.lower() in l.autor.lower()]
        return GetLibrosResponse(libros=filtrados)
    return GetLibrosResponse(libros=libros_db)


@router.get("/libro/{id}")
def get_libro(id: int) -> Libro:
    for libro in libros_db:
        if libro.id == id:
            return libro
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")


@router.post("/libro", status_code=status.HTTP_201_CREATED)
def create_libro(libro: Libro) -> CreateLibroResponse:
    for existente in libros_db:
        if existente.id == libro.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El ID ya existe")
    libros_db.append(libro)
    return CreateLibroResponse(message="Libro creado")


@router.put("/libro/{id}")
def update_libro(id: int, datos: UpdateLibroRequest) -> UpdateLibroResponse:
    for index, libro in enumerate(libros_db):
        if libro.id == id:
            actualizado = Libro(
                id=id,
                titulo=datos.titulo,
                autor=datos.autor,
                isbn=datos.isbn,
                anio=datos.anio,
            )
            libros_db[index] = actualizado
            return UpdateLibroResponse(message="Libro actualizado", libro=actualizado)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")


@router.delete("/libro/{id}")
def delete_libro(id: int) -> DeleteLibroResponse:
    for libro in libros_db:
        if libro.id == id:
            libros_db.remove(libro)
            return DeleteLibroResponse(message="Libro borrado")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")