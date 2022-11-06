import time

from calculate import calculate, CalculateAnalog
from Data import Segment, WallMaterial, Condition, Data
from UrlData import getUrl
from geocode import get_geocode, get_distance
from myparser import Parser


def get(origin):
    # print("geocode", *get_geocode(origin.address))
    page = 1
    par = Parser(getUrl(origin, get_geocode(origin.address), kfloor=0, page=page), origin)

    cnt = 0
    while True:
        for p in par:
            # print("get_distance", get_distance(origin.address, p.address))
            print(get_distance(origin.address, p.address))
            if get_distance(origin.address, p.address) > 1500: return
            # print("geocode", *get_geocode(p.address))
            yield p
            cnt += 1
        page += 1
        par.restart(getUrl(origin, get_geocode(origin.address), kfloor=0, page=page))


origin = Data(address="г. Москва, ул. Ватутина, д. 9", count_rooms=2, maximum_floor=22, floor=22,
              apartment_area=75.0,
              kitchen_area=15.0, is_balcony=True,
              condition=Condition.without_finishing, metro_distance_in_minutes=11,
              wall_material=WallMaterial.monolith,
              segment=Segment.new_building, price=0, url='')

start = time.time()
n = 10
g = get(origin)
rooms = []
try:
    for i in range(n):
        rooms.append(next(g))
except StopIteration:
    pass
print(len(rooms))
rooms.sort(key=lambda x: x.price)
for r in rooms:
    print(r.price, end=" ")
print()
print()
calcs = [CalculateAnalog(origin, rooms[i]) for i in range(len(rooms))]
calculate(calcs)
print(time.time() - start)
