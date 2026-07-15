from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, datetime

from database import get_db
from models import Showtime, Seat, BookingSeat, Screen
from schemas import ShowtimeOut, SeatOut, SeatMapOut

router = APIRouter(prefix="/api/showtimes", tags=["Showtimes"])


@router.get("", response_model=list[ShowtimeOut])
def list_showtimes(
    movie_id: Optional[int] = Query(None),
    date_filter: Optional[date] = Query(None, alias="date"),
    db: Session = Depends(get_db),
):
    query = db.query(Showtime)

    if movie_id:
        query = query.filter(Showtime.movie_id == movie_id)
    if date_filter:
        start_dt = datetime.combine(date_filter, datetime.min.time())
        end_dt = datetime.combine(date_filter, datetime.max.time())
        query = query.filter(Showtime.start_time >= start_dt, Showtime.start_time <= end_dt)

    showtimes = query.order_by(Showtime.start_time).all()
    result = []
    for st in showtimes:
        s = ShowtimeOut.model_validate(st)
        s.screen_name = st.screen.name
        result.append(s)
    return result


@router.get("/{showtime_id}/seats", response_model=SeatMapOut)
def get_seat_map(showtime_id: int, db: Session = Depends(get_db)):
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    screen = db.query(Screen).filter(Screen.id == showtime.screen_id).first()

    # Get all booked seat IDs for this showtime
    booked_seat_ids = set()
    bookings_for_showtime = showtime.bookings
    for booking in bookings_for_showtime:
        for bs in booking.booking_seats:
            booked_seat_ids.add(bs.seat_id)

    # Get all seats for this screen
    seats = db.query(Seat).filter(Seat.screen_id == screen.id).order_by(Seat.row_label, Seat.seat_number).all()

    seat_list = []
    for seat in seats:
        so = SeatOut.model_validate(seat)
        so.is_booked = seat.id in booked_seat_ids
        seat_list.append(so)

    return SeatMapOut(
        showtime_id=showtime_id,
        screen_name=screen.name,
        rows=screen.rows,
        cols=screen.cols,
        price=showtime.price,
        seats=seat_list,
    )
