from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from server.helpers.blockchain import blockchain
from server.helpers.database import student_collection

student_router = APIRouter()

class StudentInfo(BaseModel):
    id: int
    address: str
    day_of_birth: str
    email: str
    phone_number: str
    selfie_image: str
    id_front_image: str
    id_back_image: str
    root: str

@student_router.post("/submit")
async def submit(info: StudentInfo = Body(...)) -> dict:
    id = info.id
    address = info.address
    day_of_birth = info.day_of_birth
    email = info.email
    phone_number = info.phone_number
    selfie_image = info.selfie_image
    id_front_image = info.id_front_image
    id_back_image = info.id_back_image
    root = info.root

    student = student_collection.find_one({"_id": id})

    if student == None or student["status"] != "pending":
        raise HTTPException(status_code=400, detail="Invalid student id")

    update_value = {
        "$set": {
            "address": address,
            "day_of_birth": day_of_birth,
            "email": email,
            "phone_number": phone_number,
            "selfie_image": selfie_image,
            "id_front_image": id_front_image,
            "id_back_image": id_back_image,
            "root": root
        }
    }
    student_collection.update_one({"_id": id}, update=update_value)

    return {
        "message": "oke"
    }

class UpdateInfo(StudentInfo):
    signature: str

@student_router.post("/update")
async def update(info: UpdateInfo = Body(...)) -> dict:
    id = info.id
    address = info.address
    day_of_birth = info.day_of_birth
    email = info.email
    phone_number = info.phone_number
    selfie_image = info.selfie_image
    id_front_image = info.id_front_image
    id_back_image = info.id_back_image
    root = info.root
    signature = info.signature

    student = student_collection.find_one({"_id": id})

    if student == None or student["status"] == "pending":
        raise HTTPException(status_code=400, detail="Invalid student id")
    
    hash = blockchain.update_nft_info(token_id=id, root=root, signature=signature)

    update_value = {
        "$set": {
            "address": address,
            "day_of_birth": day_of_birth,
            "email": email,
            "phone_number": phone_number,
            "selfie_image": selfie_image,
            "id_front_image": id_front_image,
            "id_back_image": id_back_image,
            "root": root
        }
    }
    student_collection.update_one({"_id": id}, update=update_value)

    return {
        "message": {
            "hash": hash
        }
    }

@student_router.get("/student")
async def get_student(id: int) -> dict:
    return {
        "message": dict(student_collection.find_one({"_id" : id}) or {})
    }
