from datetime import date
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from models.libro import Libro
from models.socio import Socio


class Prestamo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    socio_id: int = Field(foreign_key="socio.id")
    libro_id: int = Field(foreign_key="libro.id")
    fecha_prestamo: date
    fecha_vencimiento: date
    fecha_devolucion: Optional[date] = Field(default=None)
    multa: int = Field(default=0)

    socio: Optional[Socio] = Relationship()
    libro: Optional[Libro] = Relationship()


class PrestamoCreate(SQLModel):
    socio_id: int
    libro_id: int


class PrestamoRead(SQLModel):
    id: int
    socio_id: int
    libro_id: int
    fecha_prestamo: date
    fecha_vencimiento: date
    fecha_devolucion: Optional[date] = None
    multa: int