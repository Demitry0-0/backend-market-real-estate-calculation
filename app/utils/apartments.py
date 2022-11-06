from datetime import datetime

from app.models import database
from app.schemas import apartments as apartments_schema

from app.schemas.users import User
from parse.Data import Data
from parse.parse import parse
from parse import calculate as calc


async def sorted_apartments(apartments: apartments_schema.ApartmentsOrigins):
    apartments.apartments.sort(key=lambda apart: apart.count_rooms)
    answer = []
    cntr = 0
    for apart in apartments.apartments:
        if apart.count_rooms != cntr:
            cntr = apart.count_rooms
            answer.append([])
        answer[-1].append(apart)
    return answer


async def add_origin(data: apartments_schema.AddOriginApartment, user: User):
    database.user_session[user.id] = database.user_session.get(user.id, dict())
    p = database.user_session[user.id][data.origin.count_rooms] = parse(
        Data(**data.origin.dict(), price=0, url=''), floor=data.search_floor, kfloor=data.kfloor,
        max_distance=data.max_distance, max_floor=data.search_max_floor
    )
    apartData = []
    try:
        for i in range(data.count):
            apartData.append(next(p))
    except StopIteration:
        pass
    return apartData


async def next_analogs(param: apartments_schema.GetNextApartments, user: User):
    if not (user.id in database.user_session and param.count_rooms in database.user_session[
        user.id]):
        return []
    p = database.user_session[user.id][param.count_rooms]
    apartData = []
    try:
        for i in range(param.count):
            apartData.append(next(p))
    except StopIteration:
        pass
    return apartData


async def calculate(data: apartments_schema.ApartmentsCalculate):
    lst = calc.analogs_to_calculate(data.origin, data.apartments, data.percentage)
    return calc.calculate(lst), calc.get_percentages(lst)
