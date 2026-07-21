from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from database import get_db
from models import Movie, Showtime, Screen, Theatre
from schemas import MovieOut, MovieListOut

router = APIRouter(prefix="/api/movies", tags=["Movies"])


@router.get("", response_model=MovieListOut)
def list_movies(
    search: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    rating: Optional[str] = Query(None),
    release_year: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Movie)

    if search:
        query = query.filter(Movie.title.ilike(f"%{search}%"))
    if genre:
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))
    if language:
        query = query.filter(Movie.language.ilike(f"%{language}%"))
    if rating:
        query = query.filter(Movie.rating.ilike(f"%{rating}%"))
    if release_year:
        query = query.filter(Movie.release_year == release_year)
    if category:
        query = query.filter(Movie.category.ilike(f"%{category}%"))

    movies = query.order_by(Movie.trending.desc(), Movie.imdb_rating.desc()).all()

    # Collect distinct filters
    all_genres = db.query(Movie.genre).distinct().all()
    genres = sorted({g[0] for g in all_genres if g[0]})

    all_languages = db.query(Movie.language).distinct().all()
    languages = sorted({l[0] for l in all_languages if l[0]})

    all_years = db.query(Movie.release_year).distinct().all()
    years = sorted({y[0] for y in all_years if y[0]}, reverse=True)

    return MovieListOut(
        movies=[MovieOut.model_validate(m) for m in movies],
        genres=genres,
    )


@router.get("/now-showing", response_model=list[MovieOut])
def now_showing(
    days: Optional[int] = Query(7, ge=1, le=30),
    db: Session = Depends(get_db),
):
    """Return movies that have showtimes from today through the next N days."""
    now = datetime.utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=days)

    # Get distinct movie IDs with showtimes in the window
    movie_ids = (
        db.query(Showtime.movie_id)
        .filter(Showtime.start_time >= start, Showtime.start_time < end)
        .distinct()
        .all()
    )
    ids = [m[0] for m in movie_ids]

    if not ids:
        return []

    movies = (
        db.query(Movie)
        .filter(Movie.id.in_(ids))
        .order_by(Movie.trending.desc(), Movie.imdb_rating.desc())
        .all()
    )
    return [MovieOut.model_validate(m) for m in movies]


@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieOut.model_validate(movie)
