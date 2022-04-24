from pydantic import BaseModel, Field, EmailStr


class ApplicationStatus(BaseModel):
    status: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "status": "ONLINE"
            }
        }
