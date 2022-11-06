from app.schemas.apartments import *
from app.schemas.users import User
from app.utils import apartments as apartments_utils
from app.utils.dependecies import get_current_user
from app.utils.read_excel import read_excel
from fastapi import APIRouter, Depends, File
from fastapi.responses import FileResponse

router = APIRouter()


@router.post("/files", response_model=ApartmentsOrigins, status_code=200)
async def create_file(file: bytes = File(), current_user: User = Depends(get_current_user)):
    with open(f"{current_user.id}.xlsx", mode="wb") as binary_file:
        binary_file.write(file)
    res = await read_excel(current_user.id)
    return ApartmentsOrigins(apartments=res)


@router.post("/choice", response_model=ResponseApartmentsOrigins, status_code=200)
async def create_post(apartments: ApartmentsOrigins, current_user: User = Depends(get_current_user)):
    resp = await apartments_utils.sorted_apartments(apartments)
    return ResponseApartmentsOrigins(apartments=[ApartmentsOrigins(apartments=res) for res in resp])


@router.post("/add", response_model=ApartmentsAnalogs, status_code=200)
async def add_orogin(origin: AddOriginApartment, current_user: User = Depends(get_current_user)):
    resp = await apartments_utils.add_origin(origin, current_user)
    return ApartmentsAnalogs(
        apartments=[ApartmentsAnalog(**apart.__dict__) for apart in resp]
    )


@router.post("/next", response_model=ApartmentsAnalogs, status_code=200)
async def next_analogs(param: GetNextApartments, current_user: User = Depends(get_current_user)):
    resp = await apartments_utils.next_analogs(param, current_user)
    return ApartmentsAnalogs(
        apartments=[ApartmentsAnalog(**apart.__dict__) for apart in resp]
    )


@router.post("/calculate", response_model=ApartmentsCalculate, status_code=200)
async def calculate(data: ApartmentsCalculate, current_user: User = Depends(get_current_user)):
    try:
        price, percentage = await apartments_utils.calculate(data)
        return ApartmentsCalculate(price=price, origin=data.origin, apartments=data.apartments,
                                   percentage=[PercentageCalculate(**p.__dict__()) for p in
                                               percentage]
                                   )
    except ZeroDivisionError:
        return {"error": "bad percentage"}


@router.get("/getfile")
async def download_file(current_user: User = Depends(get_current_user)):
    return FileResponse(f"documents/{current_user.id}.xlsx", filename=f"{current_user.name}.xlsx")
