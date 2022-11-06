from parse.table_percentage import TablePercentage
from parse.Data import Data, Condition


class PercentageCalculate:
    __slots__ = ("price", "floor", "apartment_area", "kitchen_area",
                 "balcony", "metro_distance_in_minutes", "condition")

    def __init__(self, price=0., floor=0., apartment_area=0., kitchen_area=0.,
                 balcony=0., metro_distance_in_minutes=0., condition=0.):
        self.price = price
        self.floor = floor
        self.apartment_area = apartment_area
        self.kitchen_area = kitchen_area
        self.balcony = balcony
        self.metro_distance_in_minutes = metro_distance_in_minutes
        self.condition = condition

    def __dict__(self):
        return {attr: getattr(self, attr) for attr in self.__slots__}


class CalculateAnalog:
    __slots__ = 'origin', 'analog', 'percentage', 'price_change'

    def __init__(self, origindate: Data, analogdate: Data, percentage: PercentageCalculate = None):
        self.origin = origindate
        self.analog = analogdate
        self.price_change = 0
        if percentage:
            self.percentage = percentage
            self.__calculate()
        else:
            self.percentage = PercentageCalculate()
            self.__calculate_percentage()

    @property
    def __k_prince(self) -> float:
        return TablePercentage.price / 100

    @property
    def __k_floor(self) -> float:
        def index_k_floor(date: Data):
            if date.floor == 1:
                return 0
            if date.maximum_floor == date.floor:
                return 2
            return 1

        i = index_k_floor(self.origin)
        j = index_k_floor(self.analog)
        return TablePercentage.floor[i][j] / 100

    @property
    def __k_apartment_area(self) -> float:
        def index_k_apartment_area(date: Data):
            if date.apartment_area < 30:
                return 0
            if date.apartment_area < 50:
                return 1
            if date.apartment_area < 65:
                return 2
            if date.apartment_area < 90:
                return 3
            if date.apartment_area < 120:
                return 4
            return 5

        i = index_k_apartment_area(self.origin)
        j = index_k_apartment_area(self.analog)
        return TablePercentage.apartment_area[i][j] / 100

    @property
    def __k_kitchen_area(self) -> float:
        def index_k_kitchen_area(date: Data):
            if date.kitchen_area < 7:
                return 0
            if date.kitchen_area < 10:
                return 1
            # if date.apartment_area < 15:
            return 2

        i = index_k_kitchen_area(self.origin)
        j = index_k_kitchen_area(self.analog)
        return TablePercentage.kitchen_area[i][j] / 100

    @property
    def __k_balcony(self) -> float:
        def index_k_balcony(date: Data):
            return int(date.is_balcony)

        i = index_k_balcony(self.origin)
        j = index_k_balcony(self.analog)
        return TablePercentage.balcony[i][j] / 100

    @property
    def __k_metro_distance(self) -> float:
        def index_k_metro_distance(date: Data):
            if date.metro_distance_in_minutes < 5:
                return 0
            if date.metro_distance_in_minutes < 10:
                return 1
            if date.metro_distance_in_minutes < 15:
                return 2
            if date.metro_distance_in_minutes < 30:
                return 3
            if date.metro_distance_in_minutes < 60:
                return 4
            return 5

        i = index_k_metro_distance(self.origin)
        j = index_k_metro_distance(self.analog)
        return TablePercentage.metro_distance_in_minutes[i][j] / 100

    @property
    def __condition(self) -> int:
        def index_condition(date: Data):
            if date.condition == Condition.without_finishing:
                return 0
            if date.condition == Condition.municipal_repair:
                return 1
            return 2

        i = index_condition(self.origin)
        j = index_condition(self.analog)
        return TablePercentage.condition[i][j]

    def __calculate_percentage(self):
        price = self.analog.price / self.analog.apartment_area

        self.percentage.price = self.__k_prince
        price += price * self.percentage.price

        self.percentage.apartment_area = self.__k_apartment_area
        price += price * self.percentage.apartment_area

        self.percentage.metro_distance_in_minutes = self.__k_metro_distance
        price += price * self.percentage.metro_distance_in_minutes

        self.percentage.floor = self.__k_floor
        price += price * self.percentage.floor

        self.percentage.kitchen_area = self.__k_kitchen_area
        price += price * self.percentage.kitchen_area

        self.percentage.balcony = self.__k_balcony
        price += price * self.percentage.balcony

        self.percentage.condition = self.__condition / price
        price += price * self.percentage.condition

        self.price_change = price

    def __calculate(self):
        price = self.analog.price / self.analog.apartment_area
        price += price * self.percentage.price
        price += price * self.percentage.apartment_area
        price += price * self.percentage.metro_distance_in_minutes
        price += price * self.percentage.floor
        price += price * self.percentage.kitchen_area
        price += price * self.percentage.balcony
        price += price * self.percentage.condition
        self.price_change = price

    def __dict__(self):
        return {attr: getattr(self, attr) for attr in self.__slots__}


def analogs_to_calculate(origin: Data, analogs: list, percentages: list = None):
    if not percentages:
        return [CalculateAnalog(origin, analog) for analog in analogs]
    return [CalculateAnalog(origin, analog, percen) for analog, percen in zip(analogs, percentages)]


def get_percentages(lst: list):
    return [p.percentage for p in lst]


def calculate(lst):
    # lst = [CalculateAnalog(...) for i in range(10)]
    prices = [p.price_change for p in lst]
    difference = max(prices) / min(prices) - 1.0
    # print(difference)

    k = 0.0
    ls = []
    for p in lst:
        sm = sum(map(lambda attr: abs(getattr(p.percentage, attr)), p.percentage.__slots__)) * 100
        k += 1 / sm
        ls.append(sm)
    # print(ls)

    l = []
    for p in ls:
        l.append(1 / p / k)
    # print(l)

    sm = 0
    for i in range(len(prices)):
        sm += prices[i] * l[i]
    sm = round(sm, -2)
    # print(sm)
    # print(sm * lst[0].origin.apartment_area)
    return sm * lst[0].origin.apartment_area
