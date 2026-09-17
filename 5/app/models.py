from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from .database import Base


class Enrollment(Base):
    """
    Many-to-many შუამავალი (association) ცხრილი student-სა და subject-ს შორის.
    დამატებით ინახავს გაწევრიანების თარიღს, რომელიც ავტომატურად
    ესეტება ჩანაწერის შექმნის მომენტში (server_default=func.now()).
    """
    __tablename__ = "enrollments"

    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), primary_key=True)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    student = relationship("Student", back_populates="subject_links")
    subject = relationship("Subject", back_populates="student_links")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    subject_links = relationship(
        "Enrollment", back_populates="student", cascade="all, delete-orphan"
    )


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # ხანგრძლივობა (მაგ. საათებში)

    student_links = relationship(
        "Enrollment", back_populates="subject", cascade="all, delete-orphan"
    )
