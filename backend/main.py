from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import movies, showtimes, bookings, auth, theatres, posters

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CineBook - Movie Ticket Booking", version="2.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies.router)
app.include_router(showtimes.router)
app.include_router(bookings.router)
app.include_router(auth.router)
app.include_router(theatres.router)
app.include_router(posters.router)


@app.get("/")
def root():
    return {"message": "CineBook API is running"}
