from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.status import *

router = APIRouter()


@router.get("/", response_description="Status retrieved")
async def get_status():
    status = await retrieve_status()
    return response_model(students, "Students data retrieved successfully") \
        if len(students) > 0 \
        else response_model(
        students, "Empty list returned")