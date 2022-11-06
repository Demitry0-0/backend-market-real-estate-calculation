from parse.UrlData import getUrl
from parse.geocode import get_geocode
from parse.myparser import Parser


def parse(origin, max_distance=1500, floor=0, max_floor=0, kfloor=5, ):
    page = 1
    par = Parser(getUrl(origin, get_geocode(origin.address), floor=floor,
                        kfloor=kfloor, page=page), origin,
                 search_max_floor=max_floor, max_distance=max_distance)
    for _ in range(50):
        try:
            for p in par:
                yield p
            page += 1
            par.restart(getUrl(origin, get_geocode(origin.address), kfloor=kfloor,
                               floor=floor, page=page))
        except AssertionError:
            return

