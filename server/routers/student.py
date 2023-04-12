from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from server.helpers.blockchain import blockchain
from server.helpers.database import student_collection

student_router = APIRouter()

@student_router.post("/submit")
async def submit(id: int, address: str, day_of_birth: str, email: str, phone_number: str, selfie_image: str, id_front_image: str, id_back_image: str, root: str) -> dict:
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

@student_router.post("/update")
async def update(id: int, key: str, value: str, root: str, signature: str) -> dict:
    student = student_collection.find_one({"_id": id})

    if student == None or student["status"] != "pending":
        raise HTTPException(status_code=400, detail="Invalid student id")
    
    hash = blockchain.update_nft_info(token_id=id, root=root, signature=signature)
    
    update_value = {
        "$set": {
            f"{key}": value,
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
        "message": dict(student_collection.find_one({"_id" : id}))
    }