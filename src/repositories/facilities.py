from src.models.facilities import FacilitiesOrm
from src.schemas.facilities import Facilities
from src.repositories.base import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities

