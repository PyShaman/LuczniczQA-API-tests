import motor.motor_asyncio
from bson import ObjectId
from decouple import config

from .database_helper import admin_helper, status_helper, student_helper, university_helper

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.university

admin_collection = database.get_collection('admins')
status_collection = database.get_collection('status')
student_collection = database.get_collection('students_collection')
university_collection = database.get_collection('university_collection')


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
    async for status in status_collection.find():
        statuses.append(status_helper(status))
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
