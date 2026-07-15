import random
import string

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Booking, BookingSeat, Seat, Showtime, Movie, Screen
from schemas import BookingCreate, BookingOut, BookingSeatOut

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])


def generate_booking_ref(length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))


@router.post("", response_model=BookingOut, status_code=201)
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):
    # Validate showtime exists
    showtime = db.query(Showtime).filter(Showtime.id == data.showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    # Validate all seats exist and belong to the correct screen
    seats = db.query(Seat).filter(Seat.id.in_(data.seat_ids)).all()
    if len(seats) != len(data.seat_ids):
        raise HTTPException(status_code=400, detail="One or more seats not found")

    for seat in seats:
        if seat.screen_id != showtime.screen_id:
            raise HTTPException(status_code=400, detail=f"Seat {seat.row_label}{seat.seat_number} does not belong to this screen")

    # Check seats are not already booked for this showtime (transaction-safe)
    booked = (
        db.query(BookingSeat)
        .join(Booking)
        .filter(
            Booking.showtime_id == data.showtime_id,
            BookingSeat.seat_id.in_(data.seat_ids),
        )
        .all()
    )
    if booked:
        raise HTTPException(status_code=409, detail="One or more seats are already booked")

    # Create booking
    booking_ref = generate_booking_ref()
    # Ensure uniqueness
    while db.query(Booking).filter(Booking.booking_ref == booking_ref).first():
        booking_ref = generate_booking_ref()

    total = showtime.price * len(data.seat_ids)

    booking = Booking(
        booking_ref=booking_ref,
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        customer_phone=data.customer_phone,
        showtime_id=data.showtime_id,
        total_amount=total,
    )
    db.add(booking)
    db.flush()  # Get booking.id

    for seat_id in data.seat_ids:
        bs = BookingSeat(booking_id=booking.id, seat_id=seat_id)
        db.add(bs)

    db.commit()
    db.refresh(booking)

    # Fetch with relationships
    booking = (
        db.query(Booking)
        .options(
            joinedload(Booking.booking_seats).joinedload(BookingSeat.seat),
            joinedload(Booking.showtime).joinedload(Showtime.movie),
            joinedload(Booking.showtime).joinedload(Showtime.screen),
        )
        .filter(Booking.id == booking.id)
        .first()
    )

    return _booking_to_out(booking)


@router.get("/{booking_ref}", response_model=BookingOut)
def get_booking(booking_ref: str, db: Session = Depends(get_db)):
    booking = (
        db.query(Booking)
        .options(
            joinedload(Booking.booking_seats).joinedload(BookingSeat.seat),
            joinedload(Booking.showtime).joinedload(Showtime.movie),
            joinedload(Booking.showtime).joinedload(Showtime.screen),
        )
        .filter(Booking.booking_ref == booking_ref.upper())
        .first()
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return _booking_to_out(booking)


def _booking_to_out(booking: Booking) -> BookingOut:
    return BookingOut(
        id=booking.id,
        booking_ref=booking.booking_ref,
        customer_name=booking.customer_name,
        customer_email=booking.customer_email,
        customer_phone=booking.customer_phone,
        showtime_id=booking.showtime_id,
        total_amount=booking.total_amount,
        created_at=booking.created_at,
        movie_title=booking.showtime.movie.title,
        screen_name=booking.showtime.screen.name,
        start_time=booking.showtime.start_time,
        seats=[
            BookingSeatOut(row_label=bs.seat.row_label, seat_number=bs.seat.seat_number)
            for bs in booking.booking_seats
        ],
    )
