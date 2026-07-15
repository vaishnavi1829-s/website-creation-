from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


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

    showtimes = relationship("Showtime", back_populates="movie")


class Screen(Base):
    __tablename__ = "screens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer)
    rows = Column(Integer)
    cols = Column(Integer)

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
    customer_name = Column(String(150), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(20))
    showtime_id = Column(Integer, ForeignKey("showtimes.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

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
