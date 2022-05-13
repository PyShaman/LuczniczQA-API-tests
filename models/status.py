from pydantic import BaseModel, Field


class ApplicationStatus(BaseModel):
    status: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "status": "ONLINE"
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
