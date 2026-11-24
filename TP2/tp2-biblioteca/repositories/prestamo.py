from collections.abc import Sequence
from typing import Optional
from sqlmodel import select
from database import SessionDep
from models.libro import Libro
from models.prestamo import Prestamo


class PrestamoRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_by_id(self, prestamo_id: int) -> Optional[Prestamo]:
        return self.session.get(Prestamo, prestamo_id)

    def fetch_by_socio(self, socio_id: int, activos: Optional[bool] = None) -> Sequence[Prestamo]:
        query = select(Prestamo).where(Prestamo.socio_id == socio_id)
        if activos is True:
            query = query.where(Prestamo.fecha_devolucion == None)  # noqa: E711
        elif activos is False:
            query = query.where(Prestamo.fecha_devolucion != None)  # noqa: E711
        return self.session.exec(query).all()

    def exists_by_libro(self, libro_id: int) -> bool:
        query = select(Prestamo).where(Prestamo.libro_id == libro_id)
        return self.session.exec(query).first() is not None

    def exists_by_socio(self, socio_id: int) -> bool:
        query = select(Prestamo).where(Prestamo.socio_id == socio_id)
        return self.session.exec(query).first() is not None

    def guardar(self, prestamo: Prestamo, libro: Libro) -> Prestamo:
        self.session.add(prestamo)
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(prestamo)
        return prestamo