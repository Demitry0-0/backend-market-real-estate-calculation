import random

import requests

apartment = {
    "address": "г. Москва, ул. Ватутина, д. 11",
    "count_rooms": 2,
    "maximum_floor": 22,
    "floor": 7,
    "apartment_area": 85.0,
    "kitchen_area": 15.0,
    "is_balcony": True,
    "condition": "Муниципальный ремонт",
    "metro_distance_in_minutes": 11,
    "wall_material": "панель",
    "segment": "Современное жилье"
}

data = {"apartments": [apartment.copy() for i in range(6)]}
for apart in data["apartments"]:
    apart["count_rooms"] = random.randint(1, 4)
# 974fae822a984f129dafd5ca85380979
with open("documents/1.xlsx", "rb") as f:
    byt = f.read()
request_data = {"username": "vader@deathstar.com",
                    "password": "rainbow"}
response = requests.post("http://127.0.0.1:8000/check", data=request_data
                        )
print(response.text)
