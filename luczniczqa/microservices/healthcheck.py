# TODO: simple table in db that has three fields: id, status, date.
import datetime

import aiohttp
from fastapi import APIRouter, status
from tortoise import fields
from tortoise import Model


class HealthcheckStatistics(Model):
    current_date = fields.CharField(26)
    luczniczqa_online = fields.BooleanField()


async def get_healthcheck():
    url = "http://127.0.0.1:8000/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                return await response.json(), response.status
        except Exception as ex:
            message = {"error": str(ex)}
            return message, status.HTTP_503_SERVICE_UNAVAILABLE


async def is_luczniczqa_online():
    message, status_code = await get_healthcheck()
    return True if status_code == status.HTTP_200_OK else False


router = APIRouter()


@router.get("/healthcheck")
async def get_health():
    luczniczka_status = is_luczniczqa_online()
    current_date = datetime.datetime.now()
    healthcheck_statistics = HealthcheckStatistics(current_date=current_date,
                                                   luczniczqa_online=luczniczka_status)
    return await healthcheck_statistics
