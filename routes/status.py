from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.status import *

router = APIRouter()


@router.get("/{id}", response_description="Status retrieved")
async def get_status(id):
    status = await retrieve_status(id)
    return response_model(status, "Status data retrieved successfully") \
        if len(status) > 0 \
        else response_model(
        status, "Empty list returned")
