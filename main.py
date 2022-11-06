from parse.calculate import CalculateAnalog, calculate, PercentageCalculate
from parse.Data import DataCalculate, Condition

origin = DataCalculate(full_price=0, count_rooms=2, maximum_floor=22, floor=7, apartment_area=85,
                       kitchen_area=15, is_balcony=True, metro_distance_in_minutes=11,
                       condition=Condition.municipal_repair)
analog1 = DataCalculate(28750000, 2, 24, 3, 77.4, 14, True, 10, Condition.modern_finishing)
analog2 = DataCalculate(30650000, 2, 18, 1, 84, 12, True, 14, Condition.modern_finishing)
analog3 = DataCalculate(26500000, 2, 18, 4, 64, 11.5, True, 11, Condition.modern_finishing)

a1 = CalculateAnalog(origin, analog1)
a2 = CalculateAnalog(origin, analog2)
a3 = CalculateAnalog(origin, analog3)
print(calculate([a1, a2, a3]))

"""
origin1 = Data(address="г. Москва, ул. Ватутина, д. 11", count_rooms=1, maximum_floor=22, floor=7,
               apartment_area=85,
               kitchen_area=15, is_balcony=True,
               condition=Condition.municipal_repair, metro_distance_in_minutes=11,
               wall_material=WallMaterial.panel,
               segment=Segment.modern_housing)
origin2 = Data(address="г. Москва, ул. Ватутина, д. 11", count_rooms=2, maximum_floor=22, floor=7,
               apartment_area=85,
               kitchen_area=15, is_balcony=True,
               condition=Condition.municipal_repair, metro_distance_in_minutes=11,
               wall_material=WallMaterial.panel,
               segment=Segment.modern_housing)
origin3 = Data(address="г. Москва, ул. Ватутина, д. 11", count_rooms=3, maximum_floor=22, floor=7,
               apartment_area=85,
               kitchen_area=15, is_balcony=True,
               condition=Condition.municipal_repair, metro_distance_in_minutes=11,
               wall_material=WallMaterial.panel,
               segment=Segment.modern_housing)

p1 = Parser(getUrl(origin1, get_geocode(origin1.address)))
p2 = Parser(getUrl(origin2, get_geocode(origin2.address)))
p3 = Parser(getUrl(origin3, get_geocode(origin3.address)))

start = time.time()
for _ in range(4):
    print(next(p1), next(p2), next(p3))

print(time.time() - start)
"""