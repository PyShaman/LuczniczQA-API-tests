from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.status import *

router = APIRouter()


@router.post("/", response_description="Status data added into the database")
async def add_status_data(status: ApplicationStatus = Body(...)):
    app_status = jsonable_encoder(status)
    new_status = await add_status(app_status)
    return response_model(new_status, "Status added successfully.")


@router.get("/", response_description="Status retrieved")
async def get_status():
    status = await retrieve_status()
    return response_model(status, "Status data retrieved successfully") \
        if len(status) > 0 \
        else response_model(
        status, "Empty list returned")
