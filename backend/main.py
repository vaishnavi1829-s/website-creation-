from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import movies, showtimes, bookings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Theatre Movie Booking API", version="1.0.0")

# CORS - allow all origins for development
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


@app.get("/")
def root():
    return {"message": "Theatre Movie Booking API is running"}
