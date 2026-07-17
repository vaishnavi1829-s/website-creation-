from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(255))
    full_name = Column(String(150))
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)

    bookings = relationship("Booking", back_populates="user")


class Theatre(Base):
    __tablename__ = "theatres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    location = Column(String(300), nullable=False)
    facilities = Column(Text, nullable=False)  # comma-separated
    distance_km = Column(Float, nullable=False)  # approximate distance from Salem city center

    screens = relationship("Screen", back_populates="theatre")


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    poster_url = Column(String(500))
    duration_min = Column(Integer)
    genre = Column(String(100))
    language = Column(String(50))
    rating = Column(String(10))
    release_year = Column(Integer)
    imdb_rating = Column(Float)
    trending = Column(Integer, default=0)
    category = Column(String(50), default="")

    showtimes = relationship("Showtime", back_populates="movie")


class Screen(Base):
    __tablename__ = "screens"

    id = Column(Integer, primary_key=True, index=True)
    theatre_id = Column(Integer, ForeignKey("theatres.id"), nullable=False)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer)
    rows = Column(Integer)
    cols = Column(Integer)

    theatre = relationship("Theatre", back_populates="screens")
    showtimes = relationship("Showtime", back_populates="screen")
    seats = relationship("Seat", back_populates="screen")


class Showtime(Base):
    __tablename__ = "showtimes"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)

    movie = relationship("Movie", back_populates="showtimes")
    screen = relationship("Screen", back_populates="showtimes")
    bookings = relationship("Booking", back_populates="showtime")


class Seat(Base):
    __tablename__ = "seats"
    __table_args__ = (UniqueConstraint("screen_id", "row_label", "seat_number"),)

    id = Column(Integer, primary_key=True, index=True)
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)
    row_label = Column(String(2), nullable=False)
    seat_number = Column(Integer, nullable=False)

    screen = relationship("Screen", back_populates="seats")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_ref = Column(String(10), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer_name = Column(String(150), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(20))
    showtime_id = Column(Integer, ForeignKey("showtimes.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    showtime = relationship("Showtime", back_populates="bookings")
    booking_seats = relationship("BookingSeat", back_populates="booking", cascade="all, delete-orphan")


class BookingSeat(Base):
    __tablename__ = "booking_seats"
    __table_args__ = (UniqueConstraint("booking_id", "seat_id"),)

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)

    booking = relationship("Booking", back_populates="booking_seats")
    seat = relationship("Seat")
