from datetime import datetime
from pydantic import BaseModel, EmailStr


# Student Schemas
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    class Config:
        orm_mode = True


# Course Schemas
class CourseBase(BaseModel):
    title: str
    duration: int


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int

    class Config:
        orm_mode = True


# StudentCourse Schema
class StudentCourseResponse(BaseModel):
    student_id: int
    course_id: int
    created_at: datetime

    class Config:
        orm_mode = True