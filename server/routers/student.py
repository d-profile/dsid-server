from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from server.helpers.blockchain import Blockchain
from server.helpers.database import student_collection

student_router = APIRouter()

@student_router.post("/submit")
async def submit(id: int, address: str, dob: int, email: str, phone_number: str, files: List[UploadFile] = File(...)) -> dict:
    student = student_collection.find_one({"_id": id})

    if student == None or student["status"] != "pending":
        raise HTTPException(status_code=400, detail="Invalid student id")

    if len(files) != 3:
        raise HTTPException(status_code=400, detail="Require more file")

    selfie_image = await files[0].read()
    id_front_image = await files[1].read()
    id_back_image = await files[2].read()

    update_value = {
        "$set": {
            "address": address,
            "day_of_birth": dob,
            "email": email,
            "phone_number": phone_number,
            "selfie_image": str(selfie_image),
            "id_front_image": str(id_front_image),
            "id_back_image": str(id_back_image)
        }
    }
    student_collection.update_one({"_id": id}, update=update_value)

    return {
        "message": "oke"
    }

@student_router.post("/update")
async def update() -> dict:
    return {
        "message": "oke"
    }

@student_router.get("/student")
async def get_student(id: int) -> dict:
    blockchain = Blockchain(private_key="")
    return {
        "message": dict(student_collection.find_one({"_id" : id}, {
                        "selfie_image": 0,
                        "id_front_image": 0,
                        "id_back_image": 0
                    }))
    }

@student_router.get("/student-document")
async def get_student_document(id: int) -> dict:
    return {
        "message": dict(student_collection.find_one({"_id" : id}))
    }