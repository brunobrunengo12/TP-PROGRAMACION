from collections.abc import Sequence
from typing import Annotated, Optional
from fastapi import Depends, HTTPException
from sqlmodel import select
from database import SessionDep
from models.prestamo import Prestamo
from models.socio import Socio, SocioBase


class SocioService:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_by_email(self, email: str) -> Optional[Socio]:
        query = select(Socio).where(Socio.email == email)
        return self.session.exec(query).first()

    def get_socios(self, offset: int = 0, limit: int = 100) -> Sequence[Socio]:
        query = select(Socio).offset(offset).limit(limit)
        return self.session.exec(query).all()

    def get_socio(self, socio_id: int) -> Socio:
        socio = self.session.get(Socio, socio_id)
        if not socio:
            raise HTTPException(status_code=404, detail="Socio no encontrado.")  # Regla 7
        return socio

    def create_socio(self, datos: SocioBase) -> Socio:
        if self.get_by_email(datos.email):
            raise HTTPException(status_code=409, detail="El email ya está registrado.")  # Regla 8
        nuevo_socio = Socio(
            nombre=datos.nombre,
            email=datos.email,
            activo=datos.activo,
        )
        self.session.add(nuevo_socio)
        self.session.commit()
        self.session.refresh(nuevo_socio)
        return nuevo_socio

    def update_socio(self, socio_id: int, datos: SocioBase) -> Socio:
        socio = self.get_socio(socio_id)
        if socio.email != datos.email and self.get_by_email(datos.email):
            raise HTTPException(status_code=409, detail="El email ya está registrado.")  # Regla 8
        socio.nombre = datos.nombre
        socio.email = datos.email
        socio.activo = datos.activo
        self.session.add(socio)
        self.session.commit()
        self.session.refresh(socio)
        return socio

    def delete_socio(self, socio_id: int) -> None:
        socio = self.get_socio(socio_id)
        tiene_prestamos = self.session.exec(
            select(Prestamo).where(Prestamo.socio_id == socio_id)
        ).first()
        if tiene_prestamos:
            raise HTTPException(status_code=409, detail="No se puede borrar un socio con préstamos.")
        self.session.delete(socio)
        self.session.commit()


SocioServiceDep = Annotated[SocioService, Depends()]