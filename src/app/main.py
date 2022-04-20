from fastapi import FastAPI, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from databases import Database

from .models.user import User
from .models.user import oauth2_scheme, get_current_user


app = FastAPI()
database = Database("sqlite:///test.db")


@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# @app.post("/test")
# async def fetch_data(id: int):
#     query = "SELECT * FROM tablename WHERE ID={}".format(str(id))
#     results = await database.fetch_all(query=query)
#
#     return  results