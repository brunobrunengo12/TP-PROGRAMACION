from collections.abc import Sequence
from datetime import date, timedelta
from typing import Annotated, Optional
from fastapi import Depends, HTTPException
from sqlmodel import select
from database import SessionDep
from models.libro import Libro
from models.prestamo import Prestamo
from models.socio import Socio

MAX_PRESTAMOS_ACTIVOS = 3
DIAS_PRESTAMO = 14
MULTA_POR_DIA = 100


class PrestamoService:
    def __init__(self, session: SessionDep):
        self.session = session

    def listar_prestamos(self, socio_id: int, activos: Optional[bool] = None) -> Sequence[Prestamo]:
        socio = self.session.get(Socio, socio_id)
        if not socio:
            raise HTTPException(status_code=404, detail="Socio no encontrado.")  

        query = select(Prestamo).where(Prestamo.socio_id == socio_id)
        if activos is True:
            query = query.where(Prestamo.fecha_devolucion == None)  # noqa: E711
        elif activos is False:
            query = query.where(Prestamo.fecha_devolucion != None)  # noqa: E711
        return self.session.exec(query).all()

    def crear_prestamo(self, socio_id: int, libro_id: int) -> Prestamo:
        socio = self.session.get(Socio, socio_id)
        if not socio:
            raise HTTPException(status_code=404, detail="Socio no encontrado.")  

        libro = self.session.get(Libro, libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado.")  

        if not socio.activo:
            raise HTTPException(status_code=403, detail="El socio no está activo.")  

        prestamos_activos = self.listar_prestamos(socio_id, activos=True)
        if len(prestamos_activos) >= MAX_PRESTAMOS_ACTIVOS:
            raise HTTPException(status_code=409, detail="Limite alcanzado (Maximo 3 activos).")  

        if libro.stock <= 0:
            raise HTTPException(status_code=409, detail="No hay stock del libro.")  

        hoy = date.today()
        prestamo = Prestamo(
            socio_id=socio_id,
            libro_id=libro_id,
            fecha_prestamo=hoy,
            fecha_vencimiento=hoy + timedelta(days=DIAS_PRESTAMO),  
        )
        libro.stock -= 1  

        self.session.add(prestamo)
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(prestamo)
        return prestamo

    def devolver_prestamo(self, prestamo_id: int) -> Prestamo:
        prestamo = self.session.get(Prestamo, prestamo_id)
        if not prestamo:
            raise HTTPException(status_code=404, detail="Prestamo no encontrado.")  

        if prestamo.fecha_devolucion is not None:
            raise HTTPException(status_code=409, detail="El prestamo ya fue devuelto.")  

        hoy = date.today()
        dias_atraso = (hoy - prestamo.fecha_vencimiento).days
        if dias_atraso < 0:
            dias_atraso = 0

        prestamo.fecha_devolucion = hoy
        prestamo.multa = MULTA_POR_DIA * dias_atraso  

        libro = self.session.get(Libro, prestamo.libro_id)
        libro.stock += 1  

        self.session.add(prestamo)
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(prestamo)
        return prestamo


PrestamoServiceDep = Annotated[PrestamoService, Depends()]