from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class SocioBase(SQLModel):
    nombre: str
    email: EmailStr = Field(unique=True, index=True)
    activo: bool = Field(default=True)


class Socio(SocioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class SocioCreate(SocioBase):
    pass


class SocioUpdate(SQLModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    activo: Optional[bool] = None


class SocioRead(SocioBase):
    id: int