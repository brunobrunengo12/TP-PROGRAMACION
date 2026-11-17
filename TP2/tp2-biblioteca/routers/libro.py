from typing import Annotated, Optional
from fastapi import APIRouter, Query, status
from models.libro import LibroBase, LibroRead
from services.libro import LibroServiceDep

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.post("", response_model=LibroRead, status_code=status.HTTP_201_CREATED)
def create_libro(datos: LibroBase, service: LibroServiceDep):
    return service.create_libro(datos)


@router.get("", response_model=list[LibroRead])
def get_libros(
    service: LibroServiceDep,
    disponibles: Optional[bool] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return service.get_libros(disponibles, offset, limit)


@router.get("/{libro_id}", response_model=LibroRead)
def get_libro(libro_id: int, service: LibroServiceDep):
    return service.get_libro(libro_id)


@router.put("/{libro_id}", response_model=LibroRead)
def update_libro(libro_id: int, datos: LibroBase, service: LibroServiceDep):
    return service.update_libro(libro_id, datos)


@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_libro(libro_id: int, service: LibroServiceDep):
    service.delete_libro(libro_id)


@router.post("/{libro_id}/autores/{autor_id}", response_model=LibroRead)
def asociar_autor_con_libro(libro_id: int, autor_id: int, service: LibroServiceDep):
    return service.asociar_autor(libro_id, autor_id)