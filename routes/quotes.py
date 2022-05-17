from uuid import uuid4

from fastapi import APIRouter, Body, Response
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.quotes import *

router = APIRouter()


@router.get("/", response_description="Quotes retrieved")
async def get_quotes(response: Response):
    response.headers["X-Luczniczqa"] = str(uuid4())
    quotes = await retrieve_quotes()
    if not quotes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empty quotes list.",
            headers={"X-Luczniczqa": str(uuid4())})
    else:
        return response_model(quotes, "Quotes data retrieved successfully")


@router.get("/{id}", response_description="Quote retrieved")
async def get_quote_data(id, response: Response):
    response.headers["X-Luczniczqa"] = str(uuid4())
    quote = await retrieve_quote(id)
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote with {id} doesn't exist.",
            headers={"X-Luczniczqa": str(uuid4())})
    else:
        return response_model(quote, "Quote data retrieved successfully")


@router.post("/", response_description="Quote added into the database")
async def add_quote_data(response: Response, quote: QuotesModel = Body(...)):
    response.headers["X-Luczniczqa"] = str(uuid4())
    quote = jsonable_encoder(quote)
    new_quote = await add_quote(quote)
    return response_model(new_quote, "Quote added successfully.")


@router.delete("/{id}", response_description="Quote deleted from database")
async def delete_quote_data(id: str, response: Response):
    response.headers["X-Luczniczqa"] = str(uuid4())
    deleted_quote = await delete_quote(id)
    if not deleted_quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote with {id} doesn't exist.",
            headers={"X-Luczniczqa": str(uuid4())})
    else:
        return response_model("Quote with ID: {} removed".format(id), "Quote deleted successfully")


@router.put("/{id}")
async def update_quote_data(response: Response, id: str, req: UpdateQuotesModel = Body(...)):
    response.headers["X-Luczniczqa"] = str(uuid4())
    updated_quote = await update_quote(id, req.dict())
    if not updated_quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote with {id} doesn't exist.",
            headers={"X-Luczniczqa": str(uuid4())})
    else:
        return response_model("Quote with ID: {} update is successful".format(id),
                              "Quote updated successfully")


@router.delete("/{id}", response_description="Quote deleted from database")
async def delete_quote_data(id: str, response: Response):
    response.headers["X-Lucznicz-QAt"] = str(uuid4())
    deleted_quote = await delete_quote(id)
    return response_model("Quote with ID : {} removed".format(id), "Quote deleted successfully") \
        if deleted_quote \
        else error_response_model("An error occured", 404, "Quote wit id {} doesn't exist".format(id))
