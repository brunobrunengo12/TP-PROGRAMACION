from typing import Optional
from fastapi import APIRouter, HTTPException, status
from models.users import (
    User,
    GetUsersResponse,
    CreateUserResponse,
    DeleteUserResponse,
)

router = APIRouter()

usuarios: list[User] = [
    User(id=1, name="juan perez", is_active=True),
    User(id=2, name="pepe sanchez", is_active=False),
]


@router.get("/user")
def get_users(is_active: Optional[bool] = None) -> GetUsersResponse:
    if is_active is not None:
        filtrados = [u for u in usuarios if u.is_active == is_active]
        return GetUsersResponse(users=filtrados)
    return GetUsersResponse(users=usuarios)


@router.post("/user")
def create_user(user: User) -> CreateUserResponse:
    usuarios.append(user)
    return CreateUserResponse(message="usuario creado")


@router.put("/user/{id}")
def update_user(id: int, datos: User) -> User:
    for index, user in enumerate(usuarios):
        if user.id == id:
            datos.id = id
            usuarios[index] = datos
            return datos
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado",
    )


@router.delete("/user/{id}")
def delete_user(id: int) -> DeleteUserResponse:
    for user in usuarios:
        if user.id == id:
            usuarios.remove(user)
            return DeleteUserResponse(message="usuario borrado")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado",
    )