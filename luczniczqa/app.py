from fastapi import FastAPI

from microservices.healthcheck import router as health_check_router

app = FastAPI(title="ŁuczniczQA")
app.include_router(health_check_router)