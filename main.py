from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import engine, get_db

# ვქმნით ცხრილებს ბაზაში პირველივე გაშვებაზე
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Catalog API")

# -----------------
# POST /movies
# -----------------
@app.post("/movies", response_model=schemas.MovieResponse, status_code=201)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = models.Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# -----------------
# GET /movies/search (დამატებითი ნაწილი)
# -----------------
# ყურადღება: ეს უნდა იყოს /{movie_id}-მდე, რათა Path Collision არ მოხდეს.
@app.get("/movies/search", response_model=List[schemas.MovieResponse])
def search_movies(q: str, db: Session = Depends(get_db)):
    # ilike აკეთებს case-insensitive ძიებას
    movies = db.query(models.Movie).filter(models.Movie.title.ilike(f"%{q}%")).all()
    return movies

# -----------------
# GET /movies (ფილტრაციით)
# -----------------
@app.get("/movies", response_model=List[schemas.MovieResponse])
def get_movies(
    genre: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Movie)

    if genre:
        query = query.filter(models.Movie.genre == genre)
    if year:
        query = query.filter(models.Movie.year == year)
    if min_rating is not None:
        query = query.filter(models.Movie.rating >= min_rating)
    if max_rating is not None:
        query = query.filter(models.Movie.rating <= max_rating)

    return query.all()

# -----------------
# GET /movies/{movie_id}
# -----------------
@app.get("/movies/{movie_id}", response_model=schemas.MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# -----------------
# PATCH /movies/{movie_id}
# -----------------
@app.patch("/movies/{movie_id}", response_model=schemas.MovieResponse)
def update_movie(movie_id: int, movie_update: schemas.MovieUpdate, db: Session = Depends(get_db)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # exclude_unset=True უზრუნველყოფს იმას, რომ შეიცვალოს მხოლოდ ის ველები, რომლებიც მოვიდა Request-ში
    update_data = movie_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_movie, key, value)

    db.commit()
    db.refresh(db_movie)
    return db_movie

# -----------------
# DELETE /movies/{movie_id}
# -----------------
@app.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(db_movie)
    db.commit()
    return None