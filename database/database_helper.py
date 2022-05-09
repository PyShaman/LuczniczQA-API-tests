import requests


def admin_helper(admin) -> dict:
    return {
        "id": str(admin['_id']),
        "fullname": admin['fullname'],
        "email": admin['email'],
    }


def status_helper(status) -> dict:
    return {
        "id": str(status['_id']),
        "status": status['status']
    }


def student_helper(student) -> dict:
    return {
        "id": str(student['_id']),
        "fullname": student['fullname'],
        "email": student['email'],
        "course_of_study": student['course_of_study'],
        "year": student['year'],
        "GPA": student['gpa']
    }


def university_helper(university) -> dict:
    resp = requests.get(f"http://worldtimeapi.org/api/timezone/{university['timezone']}")
    current_time = resp.json()["datetime"]

    return {
        "id": str(university['_id']),
        "name": university['name'],
        "city": university['city'],
        "timezone": university['timezone'],
        "current_time": current_time
    }


def quotes_helper(quote) -> dict:
    return {
            "id": str(quote['_id']),
            "quote": quote['quote'],
            "author": quote['author']
    }
