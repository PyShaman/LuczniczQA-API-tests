from pydantic import BaseModel, Field


class UniversityModel(BaseModel):
    name: str = Field(...)
    city: str = Field(...)
    timezone: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Poznan University of Technology",
                "city": "Poznan",
                "timezone": "Europe/Warsaw"
            }
        }


class UpdateUniversityModel(BaseModel):
    name: str = Field(...)
    city: str = Field(...)
    timezone: str = Field(...)

    class Config:
        schema_extra = {
            "hint": "List of timezones can be found here: http://worldtimeapi.org/api/timezone/",
            "example": {
                "name": "Poznan University of Technological Arts",
                "city": "Poznan",
                "timezone": "Europe/Warsaw"
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
