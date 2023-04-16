from fastapi import FastAPI
from server.routers.student import student_router
from server.routers.school import school_router
from dotenv import load_dotenv
from server.helpers.verify_sign import verify_signature
import uvicorn

app = FastAPI()
load_dotenv()

app.middleware("http")(verify_signature)

app.include_router(student_router, prefix="/students")
app.include_router(school_router, prefix="/schools")

@app.get("/")
async def root() -> dict:
    return {
        "message": "hello"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
