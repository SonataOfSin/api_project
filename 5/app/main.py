from fastapi import FastAPI

from .database import Base, engine
from .routers import students, subjects

# ცხრილების შექმნა (თუ არ არსებობს)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Students & Subjects API")

app.include_router(students.router)
app.include_router(subjects.router)
