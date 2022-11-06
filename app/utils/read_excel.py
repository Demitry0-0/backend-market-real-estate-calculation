import openpyxl
from parse.Data import Data
from app.schemas.apartments import ApartmentsOrigin


async def read_excel(user_id):
    book = openpyxl.open(f"{user_id}.xlsx", read_only=True)
    sheet = book.active
    dct = dict()
    lst = list()
    for row in range(2, sheet.max_row + 1):
        for i in range(11):
            dct[Data.__slots__[i]] = sheet[row][i].value
        lst.append(ApartmentsOrigin(**dct))
    lst.sort(key=lambda apart: apart.count_rooms)
    return lst
