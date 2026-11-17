from typing import Optional
from sqlmodel import Field, SQLModel


class LibroAutor(SQLModel, table=True):
    libro_id: Optional[int] = Field(default=None, foreign_key="libro.id", primary_key=True)
    autor_id: Optional[int] = Field(default=None, foreign_key="autor.id", primary_key=True)