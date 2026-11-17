from collections.abc import Sequence
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import select
from database import SessionDep
from models.autor import Autor, AutorBase


class AutorService:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_autores(self, offset: int = 0, limit: int = 100) -> Sequence[Autor]:
        query = select(Autor).offset(offset).limit(limit)
        return self.session.exec(query).all()

    def get_autor(self, autor_id: int) -> Autor:
        autor = self.session.get(Autor, autor_id)
        if not autor:
            raise HTTPException(status_code=404, detail="Autor no encontrado.")  # Regla 7
        return autor

    def create_autor(self, datos: AutorBase) -> Autor:
        nuevo_autor = Autor(nombre=datos.nombre, nacionalidad=datos.nacionalidad)
        self.session.add(nuevo_autor)
        self.session.commit()
        self.session.refresh(nuevo_autor)
        return nuevo_autor

    def update_autor(self, autor_id: int, datos: AutorBase) -> Autor:
        autor = self.get_autor(autor_id)
        autor.nombre = datos.nombre
        autor.nacionalidad = datos.nacionalidad
        self.session.add(autor)
        self.session.commit()
        self.session.refresh(autor)
        return autor

    def delete_autor(self, autor_id: int) -> None:
        autor = self.get_autor(autor_id)
        self.session.delete(autor)
        self.session.commit()


AutorServiceDep = Annotated[AutorService, Depends()]