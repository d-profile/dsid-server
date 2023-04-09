from fastapi import APIRouter, HTTPException
from typing import List
from pymerkle import MerkleTree
from server.helpers.database import student_collection
from server.helpers.blockchain import Blockchain

school_router = APIRouter()

@school_router.post("/create-students")
async def create_student(names: List[str], ids: List[int]) -> dict:
    if len(names) != len(ids):
        raise HTTPException(status_code=400, detail="Invalid input")

    items = []
    for i, name in enumerate(names):
        item = {
            "_id": ids[i],
            "name": name,
            "status": "pending"
        }

        items.append(item)

    student_collection.insert_many(items)

    return {
        "message": "oke"
    }

@school_router.post("/verify")
async def verify_doc(ids: List[int]) -> dict:
    students = student_collection.find({
        "_id": {
            "$in": ids
        }
    })

    addresses = []
    merkle_roots = []

    for student in students:
        tree_leaves = [student["name"], str(student["day_of_birth"]), student["email"], student["phone_number"]]
        merkle_tree = MerkleTree()
        for data in tree_leaves:
            merkle_tree.append_entry(data)

        addresses.append(student["address"])
        merkle_roots.append(str(merkle_tree.root))

    blockchain = Blo

    student_collection.update_many({
        "_id": {
            "$in": ids
        }
    }, {
        "$set": {
            "status": "verified"
        }
    })
    return {
        "message": "oke"
    }

@school_router.get("/students")
async def get_students(limit: int = 10, page: int = 1) -> dict:
    skip = limit * (page - 1)
    return {
        "message": list(student_collection.find({}, {
                        "selfie_image": 0,
                        "id_front_image": 0,
                        "id_back_image": 0
                    }).skip(skip=skip).limit(limit=limit))
    }

@school_router.post("/delete-all")
async def delete() -> dict:
    student_collection.delete_many({})
    return {
        "message": "oke"
    }