from uuid import uuid4

from fastapi import APIRouter, Body, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.student import *

router = APIRouter()


@router.get("/", response_description="Students retrieved")
async def get_students(response: Response):
    response.headers["X-Luczniczqa"] = str(uuid4())
    students = await retrieve_students()
    if not students:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empty students list.",
            headers={"X-Luczniczqa": str(uuid4())})
    else:
        return response_model(students, "Students data retrieved successfully")


@router.get("/{id}", response_description="Student data retrieved")
async def get_student_data(id, response: Response):
    response.headers["X-Luczniczqa"] = str(uuid4())
    student = await retrieve_student(id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with {id} doesn't exist.",
            headers={"X-Luczniczqa": str(uuid4())})
    else:
        return response_model(student, "Student data retrieved successfully")


@router.post("/", response_description="Student data added into the database")
async def add_student_data(response: Response, student: StudentModel = Body(...)):
    response.headers["X-Luczniczqa"] = str(uuid4())
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return response_model(new_student, "Student added successfully.")


@router.delete("/{id}", response_description="Student data deleted from the database")
async def delete_student_data(id: str, response: Response):
    response.headers["X-Luczniczqa"] = str(uuid4())
    deleted_student = await delete_student(id)
    if not deleted_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with {id} doesn't exist.",
            headers={"X-Luczniczqa": str(uuid4())})
    else:
        return response_model("Student with ID: {} removed".format(id), "Student deleted successfully")


@router.put("/{id}")
async def update_student(id: str, response: Response, req: UpdateStudentModel = Body(...)):
    response.headers["X-Luczniczqa"] = str(uuid4())
    updated_student = await update_student_data(id, req.dict())
    if not updated_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with {id} doesn't exist.",
            headers={"X-Luczniczqa": str(uuid4())})
    else:
        return response_model("Student with ID: {} update is successful".format(id),
                              "Student updated successfully")
