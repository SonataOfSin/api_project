from typing import Optional
from fastapi import FastAPI, HTTPException
from sqlalchemy import true

app = FastAPI(title="Movie Catalog API")

# საწყისი მონაცემები (In-memory storage)
MOVIES = [
    {"id": 1, "title": "The Matrix", "genre": "action", "year": 1999, "rating": 8.7},
    {"id": 2, "title": "Inception", "genre": "sci-fi", "year": 2010, "rating": 8.8},
    {"id": 3, "title": "The Hangover", "genre": "comedy", "year": 2009, "rating": 7.7},
    {"id": 4, "title": "Parasite", "genre": "drama", "year": 2019, "rating": 8.5},
    {"id": 5, "title": "Interstellar", "genre": "sci-fi", "year": 2014, "rating": 8.7},
    {"id": 6, "title": "Superbad", "genre": "comedy", "year": 2007, "rating": 7.6},
]


@app.get("/movies")
def get_movies(
    genre: Optional[str] = None,
    year: Optional[int] = None,
    min_rating: Optional[float] = None,
    search: Optional[str] = None,
):
    results = MOVIES

    # ჟანრით გაფილტვრა (case-insensitive)
    if genre:
        results = [m for m in results if m["genre"].lower() == genre.lower()]

    # წლით გაფილტვრა
    if year:
        results = [m for m in results if m["year"] == year]

    # მინიმალური რეიტინგით გაფილტვრა
    if min_rating:
        results = [m for m in results if m["rating"] >= min_rating]

    # სათაურით ძიება (case-insensitive)
    if search:
        results = [m for m in results if search.lower() in m["title"].lower()]

    return results


@app.get("/movies/{movie_id}")
def get_movie_by_id(movie_id: int):
    for movie in MOVIES:
        if movie["id"] == movie_id:
            return movie

    raise HTTPException(status_code=404, detail="Movie not found")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("movies:app", host="127.0.0.1", port=8000, reload=True)