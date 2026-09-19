from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from .database import Base


class StudentCourse(Base):
    """
    Many-to-many შუამავალი (association) ცხრილი student-სა და course-ს შორის.
    joined_at ავტომატურად ივსება ჩანაწერის შექმნის მომენტში
    (server_default=func.now()) და ხელით არ გადაეცემა.
    """
    __tablename__ = "student_courses"

    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    student = relationship("Student", back_populates="course_links")
    course = relationship("Course", back_populates="student_links")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    course_links = relationship(
        "StudentCourse", back_populates="student", cascade="all, delete-orphan"
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # ხანგრძლივობა (მაგ. საათებში)

    student_links = relationship(
        "StudentCourse", back_populates="course", cascade="all, delete-orphan"
    )
