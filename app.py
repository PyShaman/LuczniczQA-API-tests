import datetime

from pathlib import Path

from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates

from auth.jwt_bearer import JWTBearer
from database.database import status_collection, student_collection, university_collection
from routes.admin import router as admin_router
from routes.healthcheck import router as healthcheck_router
from routes.status import router as status_router
from routes.student import router as student_router
from routes.university import router as university_router
from routes.quotes import router as quotes_router


app = FastAPI(
    title="ŁuczniczQA ♥",
    description="ŁuczniczQA API will help you during the workshop with 'Introduction to API Testing in Python'",
    contact={
        "names": "Michał Bek, Jacek Stachowiak",
        "profiles": "https://www.linkedin.com/in/michal-bek/, https://www.linkedin.com/in/jacek-stachowiak-28742690/",
        "emails": "mbek@egnyte.com, jacstachowiak@egnyte.com"
    })

base_path = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(base_path / "templates"))
token_listener = JWTBearer()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to ŁuczniczQA API Testing app."}


@app.route("/start")
async def get_start(request: Request):
    refresh_time = str(datetime.datetime.now().isoformat())[:19].replace("T", " ")
    student_list = await student_collection.find({}).sort([('_id', 1)]).to_list(length=None)
    university_list = await university_collection.find({}).sort([('_id', 1)]).to_list(length=None)
    app_status_list = await status_collection.find({}).sort([('_id', 1)]).to_list(length=None)
    app_status = app_status_list[-1]["status"]
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "app_status": app_status,
                                                     "students": student_list,
                                                     "universities": university_list,
                                                     "refresh_time": refresh_time})


app.include_router(admin_router, tags=["Administrator"], prefix="/admin")
app.include_router(status_router, tags=["Status"], prefix="/status")
app.include_router(student_router, tags=["Students"], prefix="/student", dependencies=[Depends(token_listener)])
app.include_router(university_router, tags=["Universities"], prefix="/university", dependencies=[Depends(token_listener)])
app.include_router(healthcheck_router, tags=["Healthcheck"])
app.include_router(quotes_router, tags=["Quotes"], prefix="/quote")
