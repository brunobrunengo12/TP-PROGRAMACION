from collections.abc import Sequence
from typing import Optional
from sqlmodel import select
from database import SessionDep
from models.autor import Autor, AutorBase


class AutorRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def fetch_autores(self, offset: int = 0, limit: int = 100) -> Sequence[Autor]:
        query = select(Autor).offset(offset).limit(limit)
        return self.session.exec(query).all()

    def get_by_id(self, autor_id: int) -> Optional[Autor]:
        return self.session.get(Autor, autor_id)

    def create_autor(self, datos: AutorBase) -> Autor:
        nuevo_autor = Autor(nombre=datos.nombre, nacionalidad=datos.nacionalidad)
        self.session.add(nuevo_autor)
        self.session.commit()
        self.session.refresh(nuevo_autor)
        return nuevo_autor

    def update_autor(self, autor: Autor, datos: AutorBase) -> Autor:
        autor.nombre = datos.nombre
        autor.nacionalidad = datos.nacionalidad
        self.session.add(autor)
        self.session.commit()
        self.session.refresh(autor)
        return autor

    def delete_autor(self, autor: Autor) -> None:
        self.session.delete(autor)
        self.session.commit()