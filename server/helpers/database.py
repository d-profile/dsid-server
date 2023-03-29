from pymongo import MongoClient
import os

client = MongoClient(os.environ.get("MONGO_DB_URL"))
db = client.did

student_collection =  db.student_collection