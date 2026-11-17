from typing import Annotated, Optional
from fastapi import APIRouter, Query, status
from models.prestamo import PrestamoRead
from models.socio import SocioBase, SocioRead
from services.prestamo import PrestamoServiceDep
from services.socio import SocioServiceDep

router = APIRouter(prefix="/socios", tags=["Socios"])


@router.post("", response_model=SocioRead, status_code=status.HTTP_201_CREATED)
def create_socio(datos: SocioBase, service: SocioServiceDep):
    return service.create_socio(datos)


@router.get("", response_model=list[SocioRead])
def get_socios(
    service: SocioServiceDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return service.get_socios(offset, limit)


@router.get("/{socio_id}", response_model=SocioRead)
def get_socio(socio_id: int, service: SocioServiceDep):
    return service.get_socio(socio_id)


@router.put("/{socio_id}", response_model=SocioRead)
def update_socio(socio_id: int, datos: SocioBase, service: SocioServiceDep):
    return service.update_socio(socio_id, datos)


@router.delete("/{socio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_socio(socio_id: int, service: SocioServiceDep):
    service.delete_socio(socio_id)


@router.get("/{socio_id}/prestamos", response_model=list[PrestamoRead])
def get_prestamos_del_socio(
    socio_id: int,
    service: PrestamoServiceDep,
    activos: Optional[bool] = None,
):
    return service.listar_prestamos(socio_id, activos)