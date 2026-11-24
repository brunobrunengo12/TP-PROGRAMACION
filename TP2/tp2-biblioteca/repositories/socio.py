from collections.abc import Sequence
from typing import Optional
from sqlmodel import select
from database import SessionDep
from models.socio import Socio, SocioBase


class SocioRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def fetch_socios(self, offset: int = 0, limit: int = 100) -> Sequence[Socio]:
        query = select(Socio).offset(offset).limit(limit)
        return self.session.exec(query).all()

    def get_by_id(self, socio_id: int) -> Optional[Socio]:
        return self.session.get(Socio, socio_id)

    def get_by_email(self, email: str) -> Optional[Socio]:
        query = select(Socio).where(Socio.email == email)
        return self.session.exec(query).first()

    def create_socio(self, datos: SocioBase) -> Socio:
        nuevo_socio = Socio(
            nombre=datos.nombre,
            email=datos.email,
            activo=datos.activo,
        )
        self.session.add(nuevo_socio)
        self.session.commit()
        self.session.refresh(nuevo_socio)
        return nuevo_socio

    def update_socio(self, socio: Socio, datos: SocioBase) -> Socio:
        socio.nombre = datos.nombre
        socio.email = datos.email
        socio.activo = datos.activo
        self.session.add(socio)
        self.session.commit()
        self.session.refresh(socio)
        return socio

    def delete_socio(self, socio: Socio) -> None:
        self.session.delete(socio)
        self.session.commit()