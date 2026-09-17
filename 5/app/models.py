from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class StudentCourse(Base):
    __tablename__ = "student_courses"

    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="courses")
    course = relationship("Course", back_populates="students")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    courses = relationship("StudentCourse", back_populates="student")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # ხანგრძლივობა (მაგ. საათებში ან კვირებში)

    students = relationship("StudentCourse", back_populates="course")