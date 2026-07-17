from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --- Auth ---
class UserRegister(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

    model_config = {"from_attributes": True}


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class MessageOut(BaseModel):
    message: str


# --- Theatre ---
class TheatreOut(BaseModel):
    id: int
    name: str
    location: str
    facilities: str
    distance_km: float

    model_config = {"from_attributes": True}


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
    release_year: Optional[int] = None
    imdb_rating: Optional[float] = None
    trending: Optional[int] = 0
    category: Optional[str] = None

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
    theatre_name: Optional[str] = None
    theatre_location: Optional[str] = None
    theatre_facilities: Optional[str] = None

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
    theatre_name: str = ""
    theatre_location: str = ""
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
    theatre_name: Optional[str] = None
    theatre_location: Optional[str] = None
    start_time: Optional[datetime] = None
    seats: list[BookingSeatOut] = []

    model_config = {"from_attributes": True}
