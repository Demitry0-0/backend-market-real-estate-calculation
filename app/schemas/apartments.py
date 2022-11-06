from typing import List

from pydantic import BaseModel, validator, root_validator
from parse.Data import Segment, WallMaterial, Condition


class PercentageCalculate(BaseModel):
    price: float = 0.
    floor: float = 0.
    apartment_area: float = 0.
    kitchen_area: float = 0.
    balcony: float = 0.
    metro_distance_in_minutes: float = 0.
    condition: float = 0.


class ApartmentsOrigin(BaseModel):
    address: str
    count_rooms: int
    segment: Segment
    wall_material: WallMaterial
    condition: Condition
    maximum_floor: int
    floor: int
    apartment_area: float
    kitchen_area: float
    is_balcony: bool
    metro_distance_in_minutes: int

    @validator("count_rooms", pre=True)
    def parse_count_rooms(cls, value):
        if type(value) == str:
            return -1
        return value

    @validator("is_balcony", pre=True)
    def parse_is_balcony(cls, value: str):
        if type(value) == str:
            return value.lower().strip() == 'да'
        return value

    @validator("segment", pre=True)
    def parse_segment(cls, value: str):
        if isinstance(value, Segment):
            return value
        return Segment(value.strip().lower())

    @validator("wall_material", pre=True)
    def parse_wall_material(cls, value: str):
        if isinstance(value, WallMaterial):
            return value
        return WallMaterial(value.strip().lower())

    @validator("condition", pre=True)
    def parse_condition(cls, value: str):
        if isinstance(value, Condition):
            return value
        return Condition(value.strip().lower())


class ApartmentsAnalog(ApartmentsOrigin):
    price: int
    url: str


class GetNextApartments(BaseModel):
    count: int = 1
    count_rooms: int


class AddOriginApartment(BaseModel):
    origin: ApartmentsOrigin
    count: int = 3
    max_distance: int = 1500
    kfloor: int = 4
    search_floor: int = 0
    search_max_floor: int = 0


class __Counter(BaseModel):
    size: int = 0

    @root_validator(pre=False)
    def _set_fields(cls, values: dict) -> dict:
        values["size"] = len(values["apartments"])
        return values


class ApartmentsAnalogs(__Counter):
    apartments: List[ApartmentsAnalog]



class ApartmentsOrigins(__Counter):
    apartments: List[ApartmentsOrigin]


class ResponseApartmentsOrigins(__Counter):
    apartments: List[ApartmentsOrigins] = []


class ApartmentsCalculate(__Counter):
    origin: ApartmentsOrigin
    apartments: List[ApartmentsAnalog]
    percentage: List[PercentageCalculate] = None
    price: int = 0
