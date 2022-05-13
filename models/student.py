from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class StudentModel(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    course_of_study: str = Field(...)
    year: int = Field(...)
    gpa: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Miszka Kiszka",
                "email": "mkiszka@example.com",
                "course_of_study": "Highland Sheep Grazing",
                "year": 2,
                "gpa": "4.1"
            }
        }


class UpdateStudentModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    course_of_study: Optional[str]
    year: Optional[int]
    gpa: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Miszka Kiszka",
                "email": "kiszkam@example.org",
                "course_of_study": "Water resources and environmental engineering",
                "year": 4,
                "gpa": "5.0"
            }
        }


def response_model(data, message):
    return {
        "data": [
            data
        ],
        "code": 200,
        "message": message,
    }


def error_response_model(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
