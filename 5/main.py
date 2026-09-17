from fastapi import FastAPI
from app.database import engine, Base
from app.routers import students, courses

# მონაცემთა ბაზის ცხრილების შექმნა
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API")

# როუტერების რეგისტრაცია
app.include_router(students.router)
app.include_router(courses.router)


@app.get("/")
def root():
    return {"message": "API is running..."}