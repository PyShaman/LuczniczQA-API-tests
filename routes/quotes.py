from uuid import uuid4
from fastapi import APIRouter, Body, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.quotes import *

router = APIRouter()


@router.get("/{id}", response_description="Quote retrieved")
async def get_quote_data(id, response: Response):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    quote = await retrieve_quote(id)
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote with {id} doesn't exist.")
    else:
        return response_model(quote, "Quote data retrieved successfully")


@router.post("/", response_description="Quote added into the database")
async def add_quote_data(response: Response, quote: QuotesModel = Body(...)):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    quote = jsonable_encoder(quote)
    new_quote = await add_quote(quote)
    return response_model(new_quote, "Quote added successfully.")


@router.put("/{id}")
async def update_quote(response: Response, id: str, req: UpdateQuotesModel = Body(...)):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    updated_quote = await update_quote_data(id, req.dict())
    if not updated_quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote with {id} doesn't exist.")
    else:
        return response_model("Quote with ID: {} update is successful".format(id),
                              "Quote updated successfully")
