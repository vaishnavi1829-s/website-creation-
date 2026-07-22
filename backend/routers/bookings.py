import random
import string
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Booking, BookingSeat, Seat, Showtime, Movie, Screen, Theatre, User
from schemas import BookingCreate, BookingOut, BookingSeatOut
from routers.auth import get_current_user

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])


def generate_booking_ref(length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))


async def _get_optional_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> Optional[User]:
    if authorization is None or not authorization.startswith("Bearer "):
        return None
    token = authorization.removeprefix("Bearer ")
    from auth import decode_access_token
    payload = decode_access_token(token)
    if payload is None:
        return None
    user_id_str = payload.get("sub")
    if user_id_str is None:
        return None
    return db.query(User).filter(User.id == int(user_id_str)).first()


def _booking_to_out(booking: Booking) -> BookingOut:
    theatre = booking.showtime.screen.theatre
    return BookingOut(
        id=booking.id,
        booking_ref=booking.booking_ref,
        customer_name=booking.customer_name,
        customer_email=booking.customer_email,
        customer_phone=booking.customer_phone,
        showtime_id=booking.showtime_id,
        total_amount=booking.total_amount,
        payment_method=booking.payment_method,
        created_at=booking.created_at,
        movie_title=booking.showtime.movie.title,
        screen_name=booking.showtime.screen.name,
        theatre_name=theatre.name,
        theatre_location=theatre.location,
        start_time=booking.showtime.start_time,
        seats=[
            BookingSeatOut(row_label=bs.seat.row_label, seat_number=bs.seat.seat_number)
            for bs in booking.booking_seats
        ],
    )


@router.post("", response_model=BookingOut, status_code=201)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(_get_optional_user),
):
    showtime = db.query(Showtime).filter(Showtime.id == data.showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    seats = db.query(Seat).filter(Seat.id.in_(data.seat_ids)).all()
    if len(seats) != len(data.seat_ids):
        raise HTTPException(status_code=400, detail="One or more seats not found")

    for seat in seats:
        if seat.screen_id != showtime.screen_id:
            raise HTTPException(status_code=400, detail=f"Seat {seat.row_label}{seat.seat_number} does not belong to this screen")

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

    booking_ref = generate_booking_ref()
    while db.query(Booking).filter(Booking.booking_ref == booking_ref).first():
        booking_ref = generate_booking_ref()

    # Tiered pricing based on seat section
    total = 0
    for seat in seats:
        multiplier = seat.price_multiplier if seat.price_multiplier else 1.0
        total += round(showtime.price * multiplier)

    booking = Booking(
        booking_ref=booking_ref,
        user_id=current_user.id if current_user else None,
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        customer_phone=data.customer_phone,
        showtime_id=data.showtime_id,
        total_amount=total,
        payment_method=data.payment_method,
    )
    db.add(booking)
    db.flush()

    for seat_id in data.seat_ids:
        bs = BookingSeat(booking_id=booking.id, seat_id=seat_id)
        db.add(bs)

    db.commit()
    db.refresh(booking)

    booking = (
        db.query(Booking)
        .options(
            joinedload(Booking.booking_seats).joinedload(BookingSeat.seat),
            joinedload(Booking.showtime).joinedload(Showtime.movie),
            joinedload(Booking.showtime).joinedload(Showtime.screen).joinedload(Screen.theatre),
        )
        .filter(Booking.id == booking.id)
        .first()
    )

    return _booking_to_out(booking)


@router.get("/mine", response_model=list[BookingOut])
def list_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0),
):
    bookings = (
        db.query(Booking)
        .options(
            joinedload(Booking.booking_seats).joinedload(BookingSeat.seat),
            joinedload(Booking.showtime).joinedload(Showtime.movie),
            joinedload(Booking.showtime).joinedload(Showtime.screen).joinedload(Screen.theatre),
        )
        .filter(Booking.user_id == current_user.id)
        .order_by(Booking.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [_booking_to_out(b) for b in bookings]


@router.get("/{booking_ref}", response_model=BookingOut)
def get_booking(booking_ref: str, db: Session = Depends(get_db)):
    booking = (
        db.query(Booking)
        .options(
            joinedload(Booking.booking_seats).joinedload(BookingSeat.seat),
            joinedload(Booking.showtime).joinedload(Showtime.movie),
            joinedload(Booking.showtime).joinedload(Showtime.screen).joinedload(Screen.theatre),
        )
        .filter(Booking.booking_ref == booking_ref.upper())
        .first()
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return _booking_to_out(booking)
