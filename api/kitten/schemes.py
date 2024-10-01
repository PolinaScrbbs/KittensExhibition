from typing import Optional, Union
from pydantic import BaseModel

from .models import Breed, Color


class KittenForm(BaseModel):
    name: str
    description: str = "Silly Kitten"
    breed: str = Breed.BENGAL.value
    age: int = 0
    color: str = Color.WHITE.value


class KittenWithoutDetail(BaseModel):
    id: int
    name: str
    description: str


class KittenInDB(KittenWithoutDetail):
    breed: Breed
    age: int
    color: Color


class UpdateKitten(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    breed: Optional[Breed] = None
    age: Optional[int] = None
    color: Optional[Color] = None

    class Config:
        from_attributes = True


class KittenResponse(BaseModel):
    message: str = "The kitten is created"
    kitten: Union[KittenForm, KittenInDB]
