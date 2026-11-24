from collections.abc import Sequence
from typing import Optional
from sqlmodel import select
from database import SessionDep
from models.autor import Autor
from models.libro import Libro, LibroBase


class LibroRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def fetch_libros(
        self, disponibles: Optional[bool] = None, offset: int = 0, limit: int = 100
    ) -> Sequence[Libro]:
        query = select(Libro)
        if disponibles is True:
            query = query.where(Libro.stock > 0)
        elif disponibles is False:
            query = query.where(Libro.stock == 0)
        query = query.offset(offset).limit(limit)
        return self.session.exec(query).all()

    def get_by_id(self, libro_id: int) -> Optional[Libro]:
        return self.session.get(Libro, libro_id)

    def get_by_isbn(self, isbn: str) -> Optional[Libro]:
        query = select(Libro).where(Libro.isbn == isbn)
        return self.session.exec(query).first()

    def create_libro(self, datos: LibroBase) -> Libro:
        nuevo_libro = Libro(
            titulo=datos.titulo,
            isbn=datos.isbn,
            stock=datos.stock,
            anio=datos.anio,
        )
        self.session.add(nuevo_libro)
        self.session.commit()
        self.session.refresh(nuevo_libro)
        return nuevo_libro

    def update_libro(self, libro: Libro, datos: LibroBase) -> Libro:
        libro.titulo = datos.titulo
        libro.isbn = datos.isbn
        libro.stock = datos.stock
        libro.anio = datos.anio
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro

    def delete_libro(self, libro: Libro) -> None:
        self.session.delete(libro)
        self.session.commit()

    def add_autor(self, libro: Libro, autor: Autor) -> Libro:
        libro.autores.append(autor)
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro