from uuid import uuid4

from fastapi import APIRouter, Body, Response
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.student import *

router = APIRouter()


@router.get("/", response_description="Students retrieved")
async def get_students(response: Response):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    students = await retrieve_students()
    return response_model(students, "Students data retrieved successfully") \
        if len(students) > 0 \
        else response_model(
        students, "Empty list returned")


@router.get("/{id}", response_description="Student data retrieved")
async def get_student_data(id, response: Response):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    student = await retrieve_student(id)
    return response_model(student, "Student data retrieved successfully") \
        if student \
        else error_response_model("An error occured.", 404, "Student doesn't exist.")


@router.post("/", response_description="Student data added into the database")
async def add_student_data(response: Response, student: StudentModel = Body(...)):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return response_model(new_student, "Student added successfully.")


@router.delete("/{id}", response_description="Student data deleted from the database")
async def delete_student_data(id: str, response: Response):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    deleted_student = await delete_student(id)
    return response_model("Student with ID: {} removed".format(id), "Student deleted successfully") \
        if deleted_student \
        else error_response_model("An error occured", 404, "Student with id {0} doesn't exist".format(id))


@router.put("/{id}")
async def update_student(id: str, response: Response, req: UpdateStudentModel = Body(...)):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    updated_student = await update_student_data(id, req.dict())
    return response_model("Student with ID: {} name update is successful".format(id),
                          "Student name updated successfully") \
        if updated_student \
        else error_response_model("An error occurred", 404, "There was an error updating the student.".format(id))
