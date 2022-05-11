from uuid import uuid4
from fastapi import APIRouter, Body, Response
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.quotes import *

router = APIRouter()


@router.get("/{id}", response_description="Quote retrieved")
async def get_quote_data(id, response: Response):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    quote = await retrieve_quote(id)
    return response_model(quote, "Quote data retrieved successfully") \
        if quote \
        else error_response_model("An error occured.", 404, "Quote doesn't exist.")


@router.post("/", response_description="Quote added into the database")
async def add_quote_data(response: Response, quote: QuotesModel = Body(...)):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    quote = jsonable_encoder(quote)
    new_quote = await add_quote(quote)
    return response_model(new_quote, "Quote added successfully.")


@router.put("/{id}")
async def update_quote_data(response: Response, id: str, req: UpdateQuotesModel = Body(...)):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    updated_quote = await update_quote(id, req.dict())
    return response_model("Quote with ID: {} update is successful".format(id),
                          "Quote updated successfully") \
        if updated_quote \
        else error_response_model("An error occurred", 404, "There was an error updating quote {}.".format(id))


@router.delete("/{id}", response_description="Quote deleted from database")
async def delete_quote_data(id: str, response: Response):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    deleted_quote = await delete_quote(id)
    return response_model("Quote with ID : {} removed".format(id), "Quote deleted successfully") \
        if deleted_quote \
        else error_response_model("An error occured", 404, "Quote wit id {} doesn't exist".format(id))
