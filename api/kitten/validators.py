import re
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Breed, Color
from .exists import kitten_exists


class ValidateError(Exception):
    def __init__(
        self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class KittenPostValidator:
    def __init__(
        self,
        name: str,
        description: str,
        breed: str,
        age: str,
        color: str,
        session: AsyncSession,
    ) -> None:

        self.name = name
        self.description = description
        self.breed = breed
        self.age = age
        self.color = color
        self.session = session

    async def validate(self):
        try:
            await self.validate_name()
            await self.validate_description()
            await self.validate_breed()
            await self.validate_age()
            await self.validate_color()

        except ValidateError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    async def validate_name(self):
        await kitten_exists(self.session, self.name)
        if not self.name:
            raise ValidateError(
                "Username cannot be empty", status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        if not (4 <= len(self.name) <= 20):
            raise ValidateError(
                "Name must be between 4 and 20 characters long",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s]+$", self.name):
            raise ValidateError(
                "Kitten name must contain only Latin or Cyrillic letters",
                status.HTTP_400_BAD_REQUEST,
            )

    async def validate_description(self):
        if not self.description:
            raise ValidateError(
                "Description cannot be empty", status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        if len(self.description) > 200:
            raise ValidateError(
                "Description must be no more than 200 characters long",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9\s.,!?;:()\'"-]+$', self.description):
            raise ValidateError(
                "Description must contain only Latin or Cyrillic letters, numbers, and punctuation marks",
                status.HTTP_400_BAD_REQUEST,
            )

    async def validate_breed(self):
        if not self.breed:
            raise ValidateError(
                "Breed cannot be empty", status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        breed_values = await Breed.get_values()
        if self.breed not in breed_values:
            raise ValidateError("Invalid breed provided", status.HTTP_400_BAD_REQUEST)

    async def validate_age(self):
        if not self.age:
            raise ValidateError(
                "Age cannot be empty", status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        try:
            age_value = int(self.age)
            if age_value <= 0 or age_value > 6:
                raise ValidateError(
                    "Age must be a positive number and no more than 6",
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        except ValueError:
            raise ValidateError(
                "Age must be a valid integer", status.HTTP_400_BAD_REQUEST
            )

    async def validate_color(self):
        if not self.color:
            raise ValidateError(
                "Color cannot be empty", status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        color_values = await Color.get_values()
        if self.color not in color_values:
            raise ValidateError("Invalid color provided", status.HTTP_400_BAD_REQUEST)
