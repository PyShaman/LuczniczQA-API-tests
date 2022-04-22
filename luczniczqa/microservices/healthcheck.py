import aiohttp
import datetime

from dataclasses import dataclass

from fastapi import APIRouter, status


router = APIRouter()


@dataclass
class HealthcheckStatistics:

    current_date: str
    luczniczqa_online: bool


async def get_healthcheck():
    url = "http://127.0.0.1:8000"
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


@router.get("/healthcheck", tags=["healthcheck"])
async def get_health():
    luczniczqa_status = await is_luczniczqa_online()
    current_date = datetime.datetime.now()
    healthcheck_statistics = HealthcheckStatistics(current_date=current_date.isoformat(),
                                                   luczniczqa_online=luczniczqa_status)
    return healthcheck_statistics
