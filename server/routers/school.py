from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from server.helpers.database import student_collection

school_router = APIRouter()

@school_router.post("/create_students")
async def create_student(names: List[str], numbers: List[int]) -> dict:
    if len(names) != len(numbers):
        raise HTTPException(status_code=400, detail="Invalid input")

    for i, name in names:
        item = {
            "name": name,
            "number": numbers[i]
        }

        print(item)
        
        # result = student_collection.insert_one(item)
    return {
        "message": "oke"
    }