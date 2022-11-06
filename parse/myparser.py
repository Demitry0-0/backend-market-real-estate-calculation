import threading
import lxml
import chardet
import bs4.element
from requests import Session
from bs4 import BeautifulSoup
from parse.Data import Data, getSegment, getWallMaterial, getCondition


class Parser(threading.Thread):
    __slots__ = ["url", "gen", "session", "search_max_floor", "max_distance"]

    def __init__(self, url: str, data: Data, search_max_floor=0, max_distance=1500):
        super().__init__()
        self.url = url
        self.session = Session()
        self.origin = data
        self.gen = self.generate()
        self.search_max_floor = search_max_floor
        self.max_distance = max_distance

    def close(self):
        self.gen.close()
        self.join()

    def restart(self, url: str):
        self.url = url
        self.__iter__()

    def generate(self):
        def getKeyValue(key: str, value: str) -> dict:
            key = key.strip().lower()
            if key == "количество комнат":
                return {"count_rooms": int(value.strip())}
            if key == "этаж":
                return {"maximum_floor": int(value.split("/")[1]),
                        "floor": int(value.split("/")[0])
                        }
            if key == "общая площадь":
                return {"apartment_area": float(value.split()[0])}
            if key == "площадь кухни":
                return {"kitchen_area": float(value.split()[0])}
            if key == "тип здания":
                return {"wall_material": getWallMaterial(value.lower().strip())}
            if key == "год постройки":
                return {"segment": getSegment(int(value.split()[-2]))}
            if key == "тип балкона":
                return {"is_balcony": True}
            if key == "адрес":
                return {"address": value.replace("\n", " ").strip()}
            if key == "ремонт":
                return {"condition": getCondition(value.lower().strip())}
            if key == "жилая площадь":
                return {"houseroom": float(value.split()[0])}
            return {}

        def result(url, session) -> Data:
            res = session.get(url)
            soup = BeautifulSoup(res.content, 'lxml')

            info = soup.find_all('div', class_='object-info')
            if len(info) <= 3:
                return None
            dct = dict()
            dct["price"] = int(
                soup.find('span', class_="block-price_main-price-value js-price-main-value").text[
                :-1].replace(" ", ""))

            dct["is_balcony"] = False
            dct["condition"] = getCondition(None)
            for i in range(3):
                houseinfo: bs4.element.Tag = info[i].find('div')
                names = houseinfo.find_all('div',
                                           class_="object-info__details-table_property_name")
                values = houseinfo.find_all('div',
                                            class_="object-info__details-table_property_value")
                for p1, p2 in zip(names, values):
                    dct.update(getKeyValue(p1.get("title"), p2.text))

            address = soup.find('div', class_="geo-block__geo-address")
            if address and len(address.get("data-address")) > len(dct["address"]):
                dct["address"] = address.get("data-address")

            metroinfo = info[3].find('div').find('div',
                                                 class_="object-info__details-table_property_value").text
            dct["metro_distance_in_minutes"] = int(metroinfo.split()[0])
            # print()
            # print(dct.keys() ^ Data.__dict__.keys() - {'__init__', '__module__', '__repr__',
            #                                            '__slots__', '__doc__', 'get_distanse',
            #                                            'get_cords', "houseroom"})
            # print()
            if "kitchen_area" not in dct and "houseroom" in dct and "apartment_area" in dct:
                dct["kitchen_area"] = (dct["apartment_area"] - dct.pop("houseroom")) / 2
            dct["url"] = url
            try:
                d = Data(**dct)
                return d
            except TypeError:
                return None

        res = self.session.get(self.url)
        print(self.url)
        soup = BeautifulSoup(res.content, 'lxml')
        assert soup.find('div', class_="no-search no-result-similar") is None
        for quote in soup.find_all('div', class_='search-item move-object'):
            max_floor = int(quote.find('span', class_='black-text').text[:-1].split()[-1])
            link = quote.find('a', class_='search-item__title-link search-item__item-link')

            res = result("https:" + link.get("href"), self.session)

            if res:
                assert self.origin.get_distanse(res.address) <= self.max_distance

            if self.search_max_floor != 0 and max_floor != self.search_max_floor: continue

            if res is None or res.segment != self.origin.segment:
                continue
            yield res

        return

    def __iter__(self):
        self.gen = self.generate()
        return self

    def __next__(self):
        res = None
        while not res:
            res = next(self.gen)
        return res
