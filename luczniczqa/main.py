from fastapi import FastAPI

from tortoise.contrib.fastapi import register_tortoise

from microservices.auth import router as auth_router
from microservices.healthcheck import router as health_check_router

app = FastAPI(
    title="ŁuczniczQA ♥",
    description="ŁuczniczQA API will help you during the workshop with 'Introduction to API Testing in Python'",
    contact={
        "names": "Michał Bek, Jacek Stachowiak",
        "profiles": "https://www.linkedin.com/in/michal-bek/, https://www.linkedin.com/in/jacek-stachowiak-28742690/",
        "emails": "mbek@egnyte.com, jacstachowiak@egnyte.com"
    })
app.include_router(health_check_router)
app.include_router(auth_router)

register_tortoise(
    app,
    db_url='sqlite://luczniczqa/db/db.sqlite',
    modules={'models': ['microservices.auth']},
    generate_schemas=True,
    add_exception_handlers=True
)
