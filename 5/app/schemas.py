from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- Enrollment ----------

class EnrollmentBase(BaseModel):
    student_id: int
    subject_id: int


class EnrollmentOut(EnrollmentBase):
    enrolled_at: datetime

    model_config = ConfigDict(from_attributes=True)


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


# ---------- Subject ----------

class SubjectBase(BaseModel):
    title: str
    duration: int


class SubjectCreate(SubjectBase):
    pass


class SubjectOut(SubjectBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
