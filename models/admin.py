from pydantic import BaseModel, Field, EmailStr


class AdminModel(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Miszka Kiszka",
                "email": "mkiszka@example.com",
                "password": "super_secret_password"
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
