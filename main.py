from fastapi import FastAPI
from server.services.student import StudentService
import uvicorn

app = FastAPI()

@app.get("/")
async def root() -> dict:
    return {
        "message": "hello"
    }

@app.post("/student/register")
async def student_register() -> dict:
    await StudentService.register()
    return {
        "message": "ok"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)