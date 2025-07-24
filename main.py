from fastapi import FastAPI
import json
from fastapi import FastAPI, Request
from starlette.responses import Response, JSONResponse

from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/hello")
async def read_root():
    return JSONResponse (content={"message": "Hello world"}, status_code=200)

@app.get("/welcome")
def welcome_user(name : str):
    return JSONResponse({"message": f"Welcome {name}"}, status_code=200)


class StudentModel(BaseModel):
    reference: str
    firstName: str
    lastName: str
    age: int

students_store: List[StudentModel] = []

def serialized_stored_students():
    return [student.model_dump() for student in students_store]

@app.post("/students")
def add_students(new_student: List[StudentModel]):
    students_store.extend(new_student)
    return {"students": serialized_stored_students()}

@app.get("/students")
def list_students():
    return JSONResponse(content={"students": serialized_stored_students()}, status_code=200)

@app.put("/students")
def reload_students(new_student: List[StudentModel]):
    students_store.clear()
    students_store.extend(new_student)
    return  {"students": serialized_stored_students()}