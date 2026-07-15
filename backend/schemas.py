from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# --- Movie ---
class MovieOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    poster_url: Optional[str] = None
    duration_min: Optional[int] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    rating: Optional[str] = None

    model_config = {"from_attributes": True}


class MovieListOut(BaseModel):
    movies: list[MovieOut]
    genres: list[str]


# --- Showtime ---
class ShowtimeOut(BaseModel):
    id: int
    movie_id: int
    screen_id: int
    start_time: datetime
    price: float
    screen_name: Optional[str] = None

    model_config = {"from_attributes": True}


# --- Seat ---
class SeatOut(BaseModel):
    id: int
    row_label: str
    seat_number: int
    is_booked: bool = False

    model_config = {"from_attributes": True}


class SeatMapOut(BaseModel):
    showtime_id: int
    screen_name: str
    rows: int
    cols: int
    price: float
    seats: list[SeatOut]


# --- Booking ---
class BookingCreate(BaseModel):
    showtime_id: int
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    seat_ids: list[int]


class BookingSeatOut(BaseModel):
    row_label: str
    seat_number: int

    model_config = {"from_attributes": True}


class BookingOut(BaseModel):
    id: int
    booking_ref: str
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    showtime_id: int
    total_amount: float
    created_at: datetime
    movie_title: Optional[str] = None
    screen_name: Optional[str] = None
    start_time: Optional[datetime] = None
    seats: list[BookingSeatOut] = []

    model_config = {"from_attributes": True}
