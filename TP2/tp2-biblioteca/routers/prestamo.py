from fastapi import APIRouter, status
from models.prestamo import PrestamoCreate, PrestamoRead
from services.prestamo import PrestamoServiceDep

router = APIRouter(prefix="/prestamos", tags=["Prestamos"])


@router.post("", response_model=PrestamoRead, status_code=status.HTTP_201_CREATED)
def crear_prestamo(datos: PrestamoCreate, service: PrestamoServiceDep):
    return service.crear_prestamo(datos.socio_id, datos.libro_id)


@router.post("/{prestamo_id}/devolucion", response_model=PrestamoRead)
def devolver_prestamo(prestamo_id: int, service: PrestamoServiceDep):
    return service.devolver_prestamo(prestamo_id)