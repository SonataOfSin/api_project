from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- Student ----------

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class StudentCreate(StudentBase):
    pass


class StudentOut(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Course ----------

class CourseBase(BaseModel):
    title: str
    duration: int


class CourseCreate(CourseBase):
    pass


class CourseOut(CourseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- StudentCourse (Many-to-Many) ----------

class StudentCourseOut(BaseModel):
    student_id: int
    course_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)
