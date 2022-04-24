from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.university import *

router = APIRouter()


@router.get("/", response_description="Universities retrieved")
async def get_universities():
    universities = await retrieve_universities()
    return response_model(universities, "Students data retrieved successfully") \
        if len(universities) > 0 \
        else response_model(
        universities, "Empty list returned")


@router.get("/{id}", response_description="University data retrieved")
async def get_university_data(id):
    university = await retrieve_university(id)
    return response_model(university, "University data retrieved successfully") \
        if university \
        else error_response_model("An error occured.", 404, "University doesn't exist.")


@router.post("/", response_description="University data added into the database")
async def add_university_data(university: UniversityModel = Body(...)):
    university = jsonable_encoder(university)
    new_university = await add_university(university)
    return response_model(new_university, "University added successfully.")


@router.delete("/{id}", response_description="University data deleted from the database")
async def delete_university_data(id: str):
    deleted_university = await delete_university(id)
    return response_model("University with ID: {} removed".format(id), "University deleted successfully") \
        if deleted_university \
        else error_response_model("An error occured", 404, "University with id {0} doesn't exist".format(id))


@router.put("{id}")
async def update_university(id: str, req: UpdateUniversityModel = Body(...)):
    updated_university = await update_university_data(id, req.dict())
    return response_model("University with ID: {} data update is successful".format(id),
                          "University data updated successfully") \
        if updated_university \
        else error_response_model("An error occurred", 404, "There was an error updating the university.".format(id))
