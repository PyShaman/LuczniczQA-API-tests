from typing import Optional

from pydantic import BaseModel, Field


class QuotesModel(BaseModel):
    quote: str = Field(...)
    author: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "quote": "The only easy day was yesterday.",
                "author": "Navy Seals"
            }
        }


class UpdateQuotesModel(BaseModel):
    quote: Optional[str]
    author: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "quote": "The only easy day was yesterday.",
                "author": "Navy Seals."
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
