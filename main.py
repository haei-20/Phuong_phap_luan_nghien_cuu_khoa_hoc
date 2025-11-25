from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from threading import Lock

app = FastAPI(title="Student Management API")

class Student(BaseModel):
    id: int
    name: str
    age: int
    major: str

students: List[Student] = []
students_lock = Lock()  # Lock để bảo vệ list khi ghi

# GET all students
@app.get("/students", response_model=List[Student])
def get_students():
    with students_lock:  # optional nếu chỉ đọc nhưng an toàn hơn
        return students

# GET student by id
@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    with students_lock:
        for s in students:
            if s.id == student_id:
                return s
    raise HTTPException(status_code=404, detail="Student not found")

# POST create student
@app.post("/students", response_model=Student)
def create_student(student: Student):
    with students_lock:
        for s in students:
            if s.id == student.id:
                raise HTTPException(status_code=400, detail="Student ID already exists")
        students.append(student)
    return student

# PUT update student
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student):
    with students_lock:
        for idx, s in enumerate(students):
            if s.id == student_id:
                students[idx] = student
                return student
    raise HTTPException(status_code=404, detail="Student not found")

# DELETE student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with students_lock:
        for idx, s in enumerate(students):
            if s.id == student_id:
                students.pop(idx)
                return {"detail": "Student deleted"}
    raise HTTPException(status_code=404, detail="Student not found")
