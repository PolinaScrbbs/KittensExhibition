from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Breed, Color, Kitten
from .schemes import KittenForm, KittenWithoutDetail, KittenInDB, UpdateKitten
from .validators import KittenPostValidator


async def post_kitten(session: AsyncSession, kitten_data: KittenForm) -> KittenInDB:
    await KittenPostValidator(
        kitten_data.name,
        kitten_data.description,
        kitten_data.breed,
        kitten_data.age,
        kitten_data.color,
        session,
    ).validate()

    kitten = Kitten(
        name=kitten_data.name.title(),
        description=kitten_data.description,
        breed=Breed(kitten_data.breed),
        age=kitten_data.age,
        color=Color(kitten_data.color),
    )

    session.add(kitten)
    await session.commit()

    return KittenInDB(
        id=kitten.id,
        name=kitten.name,
        description=kitten.description,
        breed=kitten.breed,
        age=kitten.age,
        color=kitten.color,
    )


async def get_kittens_list(
    session: AsyncSession, breed: Optional[Breed]
) -> list[KittenWithoutDetail]:

    query = select(Kitten.id, Kitten.name, Kitten.description)
    if breed:
        query = query.where(Kitten.breed == breed)

    result = await session.execute(query)
    kittens = result.fetchall()

    if not kittens:
        raise HTTPException(status.HTTP_204_NO_CONTENT)

    return [
        KittenWithoutDetail(id=row.id, name=row.name, description=row.description)
        for row in kittens
    ]


async def get_kitten_by_id(session: AsyncSession, kitten_id: int) -> KittenInDB:
    result = await session.execute(select(Kitten).where(Kitten.id == kitten_id))

    kitten = result.scalar_one_or_none()
    if not kitten:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "The kitten was not found")

    return kitten


async def put_kitten(
    session: AsyncSession, kitten_id: int, kitten_data: UpdateKitten
) -> KittenInDB:
    kitten = await get_kitten_by_id(session, kitten_id)

    if not kitten:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "The kitten was not found")

    if kitten_data.name is not None:
        kitten.name = kitten_data.name
    if kitten_data.description is not None:
        kitten.description = kitten_data.description
    if kitten_data.breed is not None:
        kitten.breed = kitten_data.breed
    if kitten_data.age is not None:
        kitten.age = kitten_data.age
    if kitten_data.color is not None:
        kitten.color = kitten_data.color

    session.add(kitten)
    await session.commit()

    return KittenInDB(
        id=kitten.id,
        name=kitten.name,
        description=kitten.description,
        breed=kitten.breed,
        age=kitten.age,
        color=kitten.color,
    )


async def delete_kitten(session: AsyncSession, kitten_id: int):
    kitten = await get_kitten_by_id(session, kitten_id)

    if not kitten:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "The kitten was not found")

    await session.delete(kitten)
    await session.commit()
