from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import DeclarativeBase
from enum import Enum as BaseEnum


class BaseEnum(BaseEnum):
    @classmethod
    async def get_values(cls):
        return [breed.value for breed in cls]


class Breed(BaseEnum):
    ABYSSINIAN = "Abyssinian"
    BENGAL = "Bengal"
    BRITISH_SHORTHAIR = "British Shorthair"
    MAINE_COON = "Maine Coon"
    PERSIAN = "Persian"
    RAGDOLL = "Ragdoll"
    SIAMESE = "Siamese"
    SPHYNX = "Sphynx"
    SCOTTISH_FOLD = "Scottish Fold"
    BURMESE = "Burmese"
    ORIENTAL_SHORTHAIR = "Oriental Shorthair"
    NORMANDY = "Normandy"
    AMERICAN_SHORTHAIR = "American Shorthair"
    SOMALI = "Somali"
    DEVON_REX = "Devon Rex"


class Color(BaseEnum):
    BLACK = "Black"
    WHITE = "White"
    GRAY = "Gray"
    ORANGE = "Orange"
    CALICO = "Calico"
    TABBY = "Tabby"
    BROWN = "Brown"
    CREAM = "Cream"
    BLUE = "Blue"
    RED = "Red"
    CHOCOLATE = "Chocolate"
    LILAC = "Lilac"
    TORTIE = "Tortie"


class Base(DeclarativeBase):
    pass


class Kitten(Base):
    __tablename__ = "kittens"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(String(200), default="Silly Kitten", nullable=False)
    breed = Column(Enum(Breed), default=Breed.BENGAL, nullable=False)
    age = Column(Integer, default=0, nullable=False)
    color = Column(Enum(Color), default=Color.WHITE, nullable=False)
