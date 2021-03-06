from uuid import uuid4

import motor.motor_asyncio

from bson import ObjectId
from decouple import config
from fastapi import HTTPException, status

from .database_helper import admin_helper, status_helper, student_helper, university_helper, quotes_helper

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.luczniczqa

admin_collection = database.get_collection('admins')
status_collection = database.get_collection('status')
student_collection = database.get_collection('students_collection')
university_collection = database.get_collection('university_collection')
quotes_collection = database.get_collection('quotes_collection')


async def add_admin(admin_data: dict) -> dict:
    admin = await admin_collection.insert_one(admin_data)
    new_admin = await admin_collection.find_one({"_id": admin.inserted_id})
    return admin_helper(new_admin)


async def add_status(status_data: dict) -> dict:
    status = await status_collection.insert_one(status_data)
    new_status = await status_collection.find_one({"_id": status.inserted_id})
    return status_helper(new_status)


async def retrieve_status() -> dict:
    statuses = []
    async for status_ in status_collection.find():
        statuses.append(status_helper(status_))
    if not statuses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empty statuses list.",
            headers={"X-Luczniczqa": str(uuid4())})
    else:
        return statuses[-1]


async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True


async def update_student_data(id: str, data: dict):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        student_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True


async def retrieve_universities():
    universities = []
    async for university in university_collection.find():
        universities.append(university_helper(university))
    return universities


async def add_university(university_data: dict) -> dict:
    university = await university_collection.insert_one(university_data)
    new_university = await university_collection.find_one({"_id": university.inserted_id})
    return university_helper(new_university)


async def retrieve_university(id: str) -> dict:
    university = await university_collection.find_one({"_id": ObjectId(id)})
    if university:
        return university_helper(university)


async def delete_university(id: str):
    university = await university_collection.find_one({"_id": ObjectId(id)})
    if university:
        await university_collection.delete_one({"_id": ObjectId(id)})
        return True


async def update_university_data(id: str, data: dict):
    university = await university_collection.find_one({"_id": ObjectId(id)})
    if university:
        university_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True


async def retrieve_quotes():
    quotes = []
    async for quote in quotes_collection.find():
        quotes.append(quotes_helper(quote))
    return quotes


async def add_quote(quote_data: dict) -> dict:
    quote = await quotes_collection.insert_one(quote_data)
    new_quote = await quotes_collection.find_one({"_id": quote.inserted_id})
    return quotes_helper(new_quote)


async def retrieve_quote(id: str) -> dict:
    quote = await quotes_collection.find_one({"_id": ObjectId(id)})
    if quote:
        return quotes_helper(quote)


async def update_quote_data(id: str, data: dict):
    quote = await quotes_collection.find_one({"_id": ObjectId(id)})
    if quote:
        quotes_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True


async def delete_quote(id: str):
    quote = await quotes_collection.find_one({"_id": ObjectId(id)})
    if quote:
        await quotes_collection.delete_one({"_id": ObjectId(id)})
        return True
