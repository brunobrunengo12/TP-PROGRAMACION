from collections.abc import Sequence
from typing import Annotated, Optional
from fastapi import Depends, HTTPException
from sqlmodel import select
from database import SessionDep
from models.autor import Autor
from models.libro import Libro, LibroBase
from models.prestamo import Prestamo


class LibroService:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_by_isbn(self, isbn: str) -> Optional[Libro]:
        query = select(Libro).where(Libro.isbn == isbn)
        return self.session.exec(query).first()

    def get_libros(
        self, disponibles: Optional[bool] = None, offset: int = 0, limit: int = 100
    ) -> Sequence[Libro]:
        query = select(Libro)
        if disponibles is True:
            query = query.where(Libro.stock > 0)
        elif disponibles is False:
            query = query.where(Libro.stock == 0)
        query = query.offset(offset).limit(limit)
        return self.session.exec(query).all()

    def get_libro(self, libro_id: int) -> Libro:
        libro = self.session.get(Libro, libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado.")  # Regla 7
        return libro

    def create_libro(self, datos: LibroBase) -> Libro:
        if self.get_by_isbn(datos.isbn):
            raise HTTPException(status_code=409, detail="El ISBN ya está registrado.")  # Regla 8
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

    def update_libro(self, libro_id: int, datos: LibroBase) -> Libro:
        libro = self.get_libro(libro_id)
        if libro.isbn != datos.isbn and self.get_by_isbn(datos.isbn):
            raise HTTPException(status_code=409, detail="El ISBN ya está registrado.")  # Regla 8
        libro.titulo = datos.titulo
        libro.isbn = datos.isbn
        libro.stock = datos.stock
        libro.anio = datos.anio
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro

    def delete_libro(self, libro_id: int) -> None:
        libro = self.get_libro(libro_id)
        tiene_prestamos = self.session.exec(
            select(Prestamo).where(Prestamo.libro_id == libro_id)
        ).first()
        if tiene_prestamos:
            raise HTTPException(status_code=409, detail="No se puede borrar un libro con préstamos.")
        self.session.delete(libro)
        self.session.commit()

    def asociar_autor(self, libro_id: int, autor_id: int) -> Libro:
        libro = self.get_libro(libro_id)
        autor = self.session.get(Autor, autor_id)
        if not autor:
            raise HTTPException(status_code=404, detail="Autor no encontrado.")  # Regla 7
        if autor in libro.autores:
            raise HTTPException(status_code=409, detail="El autor ya está asociado al libro.")
        libro.autores.append(autor)
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro


LibroServiceDep = Annotated[LibroService, Depends()]