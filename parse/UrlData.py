from parse.Data import WallMaterial, Segment, Data


# param
# param
def __param(limit=100, page=1):
    return f"page={page}&limit={limit}"


# param
# ?rooms%5B0%5D=4
def __room(cnt: int):  # -1 ->студия
    return f"rooms%5B0%5D={cnt}"


# param
# ? subcategory=1
def __category(): return "subcategory=1"


# param
# ? sort=3&lat_user={lat}&lng_user={lng}
def __sort(lat: float, lng: float):
    return f"sort=3&lat_user={lat}&lng_user={lng}"


# url
# /v_kirpichnom_dome/
def __wallmaterial(wall: WallMaterial):
    if wall == WallMaterial.monolith:
        return "v_monolitnom_dome/"
    if wall == WallMaterial.brick:
        return "v_kirpichnom_dome/"
    if wall == WallMaterial.panel:
        return "v_panelnom_dome/"
    return "/"


# url
def __floor(floor, k):
    mn, mx = (max(floor - k, 1), floor + k)
    if mn > mx: mn, mx = mx, mn
    return f"floor_min={mn}&floor_max={mx}"


# url
# /vtorichnaya/
def __segment(seg: Segment):
    if seg == Segment.new_building:
        return "kvartiry_v_novostroykah/"
    return "kvartiry/vtorichnaya/"


def getUrl(data: Data, cords: tuple, limit=30, page=1, kfloor=5, floor=0):
    if not floor:
        floor = data.floor
    return "https://move.ru/{}{}?{}&{}&{}&{}&{}".format(__segment(data.segment),
                                                        __wallmaterial(data.wall_material),
                                                        __floor(floor, kfloor),
                                                        __category(), __room(data.count_rooms),
                                                        __param(limit, page), __sort(*cords))
