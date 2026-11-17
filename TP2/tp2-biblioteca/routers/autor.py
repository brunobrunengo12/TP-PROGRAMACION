from typing import Annotated
from fastapi import APIRouter, Query, status
from models.autor import AutorBase, AutorRead
from services.autor import AutorServiceDep

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.post("", response_model=AutorRead, status_code=status.HTTP_201_CREATED)
def create_autor(datos: AutorBase, service: AutorServiceDep):
    return service.create_autor(datos)


@router.get("", response_model=list[AutorRead])
def get_autores(
    service: AutorServiceDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return service.get_autores(offset, limit)


@router.get("/{autor_id}", response_model=AutorRead)
def get_autor(autor_id: int, service: AutorServiceDep):
    return service.get_autor(autor_id)


@router.put("/{autor_id}", response_model=AutorRead)
def update_autor(autor_id: int, datos: AutorBase, service: AutorServiceDep):
    return service.update_autor(autor_id, datos)


@router.delete("/{autor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_autor(autor_id: int, service: AutorServiceDep):
    service.delete_autor(autor_id)