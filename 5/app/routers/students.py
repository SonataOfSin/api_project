from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/students", tags=["Students"])


# ---------- CRUD ----------

@router.post("", response_model=schemas.StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(payload: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = models.Student(**payload.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("", response_model=list[schemas.StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@router.get("/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    db.delete(student)
    db.commit()


# ---------- Many-to-Many ----------

@router.post(
    "/{student_id}/courses/{course_id}",
    response_model=schemas.StudentCourseOut,
    status_code=status.HTTP_201_CREATED,
)
def enroll_student_in_course(student_id: int, course_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    existing = db.query(models.StudentCourse).filter(
        models.StudentCourse.student_id == student_id,
        models.StudentCourse.course_id == course_id,
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already enrolled in this course",
        )

    # joined_at ავტომატურად ივსება Model-ის server_default-ით
    enrollment = models.StudentCourse(student_id=student_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get("/{student_id}/courses", response_model=list[schemas.CourseOut])
def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return [link.course for link in student.course_links]


@router.delete("/{student_id}/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_student_from_course(student_id: int, course_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(models.StudentCourse).filter(
        models.StudentCourse.student_id == student_id,
        models.StudentCourse.course_id == course_id,
    ).first()
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
