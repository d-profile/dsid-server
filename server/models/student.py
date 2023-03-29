from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class StudentSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)