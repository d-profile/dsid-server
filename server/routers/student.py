from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from server.helpers.database import student_collection

student_router = APIRouter()

@student_router.post("/submit")
async def submit(student_number: int, address: str, files: List[UploadFile] = File(...)) -> dict:
    if len(files) != 3:
        raise HTTPException(status_code=400, detail="Require more file")

    selfie_image = await files[0].read()
    id_front_image = await files[1].read()
    id_back_image = await files[2].read()

    item = {
        "address": address,
        "student_number": student_number,
        "selfie_image": selfie_image,
        "id_front_image": id_front_image,
        "id_back_image": id_back_image
    }

    result = student_collection.insert_one(item)

    return {
        "message": "oke"
    }
