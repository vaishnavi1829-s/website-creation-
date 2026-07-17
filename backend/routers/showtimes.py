from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, datetime

from database import get_db
from models import Showtime, Seat, BookingSeat, Screen, Theatre
from schemas import ShowtimeOut, SeatOut, SeatMapOut

router = APIRouter(prefix="/api/showtimes", tags=["Showtimes"])


@router.get("", response_model=list[ShowtimeOut])
def list_showtimes(
    movie_id: Optional[int] = Query(None),
    date_filter: Optional[date] = Query(None, alias="date"),
    theatre_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Showtime)

    if movie_id:
        query = query.filter(Showtime.movie_id == movie_id)
    if date_filter:
        start_dt = datetime.combine(date_filter, datetime.min.time())
        end_dt = datetime.combine(date_filter, datetime.max.time())
        query = query.filter(Showtime.start_time >= start_dt, Showtime.start_time <= end_dt)
    if theatre_id:
        query = query.join(Screen).filter(Screen.theatre_id == theatre_id)

    showtimes = query.order_by(Showtime.start_time).all()
    result = []
    for st in showtimes:
        s = ShowtimeOut.model_validate(st)
        s.screen_name = st.screen.name
        s.theatre_name = st.screen.theatre.name
        s.theatre_location = st.screen.theatre.location
        s.theatre_facilities = st.screen.theatre.facilities
        result.append(s)
    return result


@router.get("/{showtime_id}/seats", response_model=SeatMapOut)
def get_seat_map(showtime_id: int, db: Session = Depends(get_db)):
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    screen = db.query(Screen).filter(Screen.id == showtime.screen_id).first()
    theatre = db.query(Theatre).filter(Theatre.id == screen.theatre_id).first()

    # Get all booked seat IDs for this showtime
    booked_seat_ids = set()
    for booking in showtime.bookings:
        for bs in booking.booking_seats:
            booked_seat_ids.add(bs.seat_id)

    seats = db.query(Seat).filter(Seat.screen_id == screen.id).order_by(Seat.row_label, Seat.seat_number).all()

    seat_list = []
    for seat in seats:
        so = SeatOut.model_validate(seat)
        so.is_booked = seat.id in booked_seat_ids
        seat_list.append(so)

    return SeatMapOut(
        showtime_id=showtime_id,
        screen_name=screen.name,
        theatre_name=theatre.name,
        theatre_location=theatre.location,
        rows=screen.rows,
        cols=screen.cols,
        price=showtime.price,
        seats=seat_list,
    )
