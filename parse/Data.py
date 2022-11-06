import enum
from datetime import datetime

from parse.geocode import get_geocode, get_distance


class Segment(enum.Enum):
    new_building = "новостройка"
    modern_housing = "современное жилье"
    old_housing_stock = "старый жилой фонд"


def getSegment(years: int) -> Segment:
    if years <= 1990:
        return Segment.old_housing_stock
    if datetime.now().year - years <= 1:
        return Segment.new_building
    return Segment.modern_housing


class WallMaterial(enum.Enum):
    brick = "кирпич"
    panel = "панель"
    monolith = "монолит"


def getWallMaterial(wall: str) -> WallMaterial:
    if WallMaterial.monolith.value in wall:
        return WallMaterial.monolith
    if WallMaterial.panel.value in wall:
        return WallMaterial.panel
    return WallMaterial.brick


class Condition(enum.Enum):
    without_finishing = "без отделки"
    municipal_repair = "муниципальный ремонт"
    modern_finishing = "современная отделка"


def getCondition(con: str):
    if con is None:
        return Condition.municipal_repair
    if con == Condition.without_finishing.value:
        return Condition.without_finishing
    return Condition.municipal_repair


class Data():
    __slots__ = ("address", "count_rooms", "segment", "maximum_floor",
                 "wall_material", "floor", "apartment_area",
                 "kitchen_area", "is_balcony", "metro_distance_in_minutes", "condition", "price",
                 "url")

    def __init__(self, address: str, count_rooms: int, segment: Segment, maximum_floor: int,
                 wall_material: WallMaterial, floor: int, apartment_area: float, kitchen_area: float,
                 is_balcony: bool, metro_distance_in_minutes: int, condition: Condition,
                 price: int, url, **kwargs):
        self.address = address  # 1
        self.count_rooms = count_rooms  # 1
        self.segment = segment  #
        self.maximum_floor = maximum_floor  # 1
        self.wall_material = wall_material  # 1
        self.floor = floor  # 1
        self.apartment_area = apartment_area  # 1
        self.kitchen_area = kitchen_area  # 1
        self.is_balcony = is_balcony  # 1
        self.metro_distance_in_minutes = metro_distance_in_minutes  # 1
        self.condition = condition  # 1
        self.price = price
        self.url = url

    def get_cords(self):
        return get_geocode(self.address)

    def get_distanse(self, address):
        return get_distance(self.address, address)

    @property
    def __dict__(self) -> dict:
        return {attr: getattr(self, attr) for attr in self.__slots__}

    def __repr__(self):
        return self.__dict__.__str__()


class DataCalculate:
    __slots__ = ("price", "count_rooms", "maximum_floor",
                 "floor", "apartment_area",
                 "kitchen_area", "is_balcony", "metro_distance_in_minutes", "condition")

    def __init__(self, full_price: int,
                 count_rooms: int, maximum_floor: int,
                 floor: int, apartment_area: float,
                 kitchen_area: float, is_balcony: bool, metro_distance_in_minutes: float,
                 condition: Condition):
        self.price = full_price
        self.count_rooms = count_rooms  # ?
        self.maximum_floor = maximum_floor  # @
        self.floor = floor  # @
        self.apartment_area = apartment_area  # @
        self.kitchen_area = kitchen_area  # @
        self.is_balcony = is_balcony  # @
        self.metro_distance_in_minutes = metro_distance_in_minutes  # @
        self.condition = condition  # @
