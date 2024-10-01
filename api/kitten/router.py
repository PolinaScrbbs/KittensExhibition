from typing import List, Optional
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from .models import Breed
from .schemes import (
    KittenForm,
    KittenInDB,
    KittenWithoutDetail,
    UpdateKitten,
    KittenResponse,
)
from . import queries as qr

router = APIRouter(prefix="/kittens")


@router.get("/breeds/")
async def get_breeds():
    values = await Breed.get_values()
    return values


@router.post("/", response_model=KittenResponse)
async def create_kitten(
    kitten_data: KittenForm, session: AsyncSession = Depends(get_session)
) -> KittenResponse:
    created_kitten = await qr.post_kitten(session, kitten_data)
    return KittenResponse(kitten=created_kitten)


@router.get("/", response_model=List[KittenWithoutDetail])
async def get_kittens_list(
    breed: Optional[Breed] = None, session: AsyncSession = Depends(get_session)
) -> List[KittenWithoutDetail]:
    kittens = await qr.get_kittens_list(session, breed)
    return kittens


@router.get("/{kitten_id}/", response_model=KittenInDB)
async def get_kitten(
    kitten_id: int, session: AsyncSession = Depends(get_session)
) -> KittenInDB:
    kitten = await qr.get_kitten_by_id(session, kitten_id)
    return kitten


@router.put("/kittens/{kitten_id}/", response_model=KittenResponse)
async def update_kitten(
    kitten_id: int,
    kitten_data: UpdateKitten,
    session: AsyncSession = Depends(get_session),
) -> KittenResponse:
    kitten = await qr.put_kitten(session, kitten_id, kitten_data)

    return KittenResponse(message="The kitten has been updated", kitten=kitten)


@router.delete("/kittens/{kitten_id}/")
async def delete_kitten(
    kitten_id: int, session: AsyncSession = Depends(get_session)
) -> str:
    await qr.delete_kitten(session, kitten_id)
    return "The kitten has been deleted"
