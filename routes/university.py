from uuid import uuid4

from fastapi import APIRouter, Body, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.university import *

router = APIRouter()


@router.get("/", response_description="Universities retrieved")
async def get_universities(response: Response):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    universities = await retrieve_universities()
    return response_model(universities, "Students data retrieved successfully") \
        if len(universities) > 0 \
        else HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empty universities list.")


@router.get("/{id}", response_description="University data retrieved")
async def get_university_data(id, response: Response):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    university = await retrieve_university(id)
    return response_model(university, "University data retrieved successfully") \
        if university \
        else HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"University with {id} doesn't exist.")


@router.post("/", response_description="University data added into the database")
async def add_university_data(response: Response, university: UniversityModel = Body(...)):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    university = jsonable_encoder(university)
    new_university = await add_university(university)
    return response_model(new_university, "University added successfully.")


@router.delete("/{id}", response_description="University data deleted from the database")
async def delete_university_data(id: str, response: Response):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    deleted_university = await delete_university(id)
    return response_model("University with ID: {} removed".format(id), "University deleted successfully") \
        if deleted_university \
        else HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"University with {id} doesn't exist.")


@router.put("/{id}")
async def update_university(id: str, response: Response, req: UpdateUniversityModel = Body(...)):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    updated_university = await update_university_data(id, req.dict())
    return response_model("University with ID: {} data update is successful".format(id),
                          "University data updated successfully") \
        if updated_university \
        else HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"University with {id} doesn't exist.")
