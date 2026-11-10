from pydantic import BaseModel, Field
from typing import List
 
 
class Libro(BaseModel):
    id: int
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    isbn: str = Field(min_length=1)
    anio: int = Field(ge=0, le=2100)
 
 
class UpdateLibroRequest(BaseModel):
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    isbn: str = Field(min_length=1)
    anio: int = Field(ge=0, le=2100)
 
 
class GetLibrosResponse(BaseModel):
    libros: List[Libro]
 
 
class CreateLibroResponse(BaseModel):
    message: str
 
 
class UpdateLibroResponse(BaseModel):
    message: str
    libro: Libro
 
 
class DeleteLibroResponse(BaseModel):
    message: str
 