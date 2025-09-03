from pydantic import BaseModel, ConfigDict


class FacilitiesAdd(BaseModel):
    title: str

class Facilities(FacilitiesAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomsFacilityAdd(BaseModel):
    rooms_id: int
    facility_id: int


class RoomsFacility(RoomsFacilityAdd):
    id: int