from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Theatre
from schemas import TheatreOut

router = APIRouter(prefix="/api/theatres", tags=["Theatres"])


@router.get("", response_model=list[TheatreOut])
def list_theatres(db: Session = Depends(get_db)):
    return db.query(Theatre).order_by(Theatre.name).all()
