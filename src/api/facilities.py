from fastapi import APIRouter
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["удобства"])


@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def add_facility(db: DBDep, facilities_data: FacilitiesAdd):
    await db.facilities.add(data=facilities_data)
    await  db.commit()

    return {"statys": "OK"}
