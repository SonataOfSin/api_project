import os
import sys

# საშუალებას აძლევს გაშვებას პირდაპირ სკრიპტადაც: python app/main.py
# (უზრუნველყოფს, რომ "app" პაკეტი import-იბოდეს თუ ვიწყებთ ფაილს უშუალოდ)
if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import students, courses

# ცხრილების შექმნა (თუ არ არსებობს)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Students & Courses API")

app.include_router(students.router)
app.include_router(courses.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
