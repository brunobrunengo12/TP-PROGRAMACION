from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel
from models.libro_autor import LibroAutor

if TYPE_CHECKING:
    from models.libro import Libro


class AutorBase(SQLModel):
    nombre: str
    nacionalidad: str


class Autor(AutorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    libros: List["Libro"] = Relationship(back_populates="autores", link_model=LibroAutor)


class AutorCreate(AutorBase):
    pass


class AutorUpdate(SQLModel):
    nombre: Optional[str] = None
    nacionalidad: Optional[str] = None


class AutorRead(AutorBase):
    id: int