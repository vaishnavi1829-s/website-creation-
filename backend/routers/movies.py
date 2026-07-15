from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models import Movie
from schemas import MovieOut, MovieListOut

router = APIRouter(prefix="/api/movies", tags=["Movies"])


@router.get("", response_model=MovieListOut)
def list_movies(
    search: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Movie)

    if search:
        query = query.filter(Movie.title.ilike(f"%{search}%"))
    if genre:
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))

    movies = query.all()

    # Collect distinct genres for filter
    all_genres = db.query(Movie.genre).distinct().all()
    genres = sorted({g[0] for g in all_genres if g[0]})

    return MovieListOut(
        movies=[MovieOut.model_validate(m) for m in movies],
        genres=genres,
    )


@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieOut.model_validate(movie)
