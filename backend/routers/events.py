from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Optional
import hashlib

from database import SessionLocal, get_db
from models import Event
from schemas import EventOut, EventListOut

router = APIRouter(prefix="/api/events", tags=["Events"])


# ── SVG Poster Generation ──

KIDS_CFG = {
    "bg": ("#ff6b6b", "#ee5a24", "#ff6348"),
    "accent": "#ffd700", "text_accent": "#ffe066",
    "icon": "🧒", "mood": "KIDS ZONE",
}
MUSIC_CFG = {
    "bg": ("#1a0533", "#4c1d95", "#2e1065"),
    "accent": "#c084fc", "text_accent": "#d8b4fe",
    "icon": "🎵", "mood": "LIVE MUSIC",
}
COMEDY_CFG = {
    "bg": ("#451a03", "#b45309", "#78350f"),
    "accent": "#fbbf24", "text_accent": "#fde68a",
    "icon": "😂", "mood": "COMEDY NIGHT",
}
CFG_MAP = {"kids": KIDS_CFG, "music": MUSIC_CFG, "comedy": COMEDY_CFG}


def _hc(seed, off=0):
    h = int(hashlib.md5(seed.encode()).hexdigest()[:6], 16)
    r = ((h >> 16) & 0xFF + off) % 256
    g = ((h >> 8) & 0xFF + off) % 256
    b = ((h >> 0) & 0xFF + off) % 256
    return f"#{r:02x}{g:02x}{b:02x}"


def _poster(event):
    cfg = CFG_MAP.get(event.category, KIDS_CFG)
    t = event.title or "Untitled"
    art = event.artist_name or ""
    ven = event.venue or ""
    cit = event.city or ""

    ed = ""
    if event.event_date:
        d = event.event_date
        ms = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
        ed = f"{d.day} {ms[d.month-1]} {d.year}"
    et = event.event_time or ""
    pr = f"Rs.{int(event.price):,}" if event.price else ""
    rt = f"{event.rating:.1f}" if event.rating else ""
    lang = event.language or ""
    age = event.age_recommendation or ""
    a2 = _hc(t, 30)
    a3 = _hc(t, -20)

    disp = t if len(t) <= 26 else t[:23] + "..."
    lines = []
    if len(disp) > 14:
        mid = disp.rfind(" ", 0, len(disp)//2+5)
        if mid < 5: mid = len(disp)//2
        lines = [disp[:mid].strip(), disp[mid:].strip()]
    else:
        lines = [disp]

    ty = 210
    tfs = 28 if len(lines) == 1 else 24
    ts = ""
    for i, l in enumerate(lines):
        ts += f'<text x="210" y="{ty+i*36}" text-anchor="middle" fill="#fff" font-size="{tfs}" font-weight="900" font-family="Georgia,serif" letter-spacing="2" filter="url(#tsh)">{l}</text>\n'

    ay = ty + len(lines)*36 + 18
    a_svg = f'<text x="210" y="{ay}" text-anchor="middle" fill="{cfg["text_accent"]}" font-size="15" font-weight="600" font-family="sans-serif" letter-spacing="0.5" opacity="0.9">{art}</text>\n' if art else ""

    iy = ay + 28
    it = f"{ven}, {cit}" if not ed else (f"{ed} - {et}" if et else ed)
    i_svg = f'<text x="210" y="{iy}" text-anchor="middle" fill="rgba(255,255,255,0.65)" font-size="13" font-family="sans-serif" letter-spacing="0.5">{it}</text>\n'

    by = iy + 38
    bits = []
    if lang: bits.append(lang)
    if age and event.category == "kids": bits.append(f"Ages {age}")
    elif rt: bits.append(f"* {rt}")
    if pr: bits.append(pr)

    bw, bgap = 95, 35
    tw = len(bits)*bw + (len(bits)-1)*bgap
    sx = 210 - tw//2
    b_svg = ""
    for i, item in enumerate(bits[:3]):
        bx = sx + i*(bw+bgap)
        b_svg += (
            f'<rect x="{bx}" y="{by}" width="{bw}" height="30" rx="15" fill="{cfg["accent"]}" opacity="0.15" stroke="{cfg["accent"]}" stroke-width="1" stroke-opacity="0.35"/>\n'
            f'<text x="{bx+bw/2}" y="{by+20}" text-anchor="middle" fill="{cfg["text_accent"]}" font-size="12" font-weight="700" font-family="sans-serif" letter-spacing="0.5">{item}</text>\n'
        )

    cy = by + 60
    cs = (
        f'<rect x="100" y="{cy}" width="220" height="48" rx="24" fill="url(#ag)" filter="url(#sg)"/>\n'
        f'<text x="210" y="{cy+32}" text-anchor="middle" fill="#fff" font-size="17" font-weight="800" font-family="sans-serif" letter-spacing="2">BOOK NOW *</text>\n'
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="630" viewBox="0 0 420 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{cfg['bg'][0]}"/><stop offset="50%" stop-color="{cfg['bg'][1]}"/><stop offset="100%" stop-color="{cfg['bg'][2]}"/>
    </linearGradient>
    <linearGradient id="ag" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{cfg['accent']}"/><stop offset="100%" stop-color="{a2}"/>
    </linearGradient>
    <filter id="glw" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="tsh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="2" dy="3" stdDeviation="3" flood-color="#000" flood-opacity="0.8"/></filter>
    <filter id="sg"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <pattern id="dot" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="8" cy="8" r="1" fill="rgba(255,255,255,0.06)"/></pattern>
  </defs>
  <rect width="420" height="630" fill="url(#bg)"/><rect width="420" height="630" fill="url(#dot)"/>
  <circle cx="380" cy="80" r="120" fill="{cfg['accent']}" opacity="0.06"/>
  <circle cx="40" cy="520" r="140" fill="{cfg['accent']}" opacity="0.06"/>
  <circle cx="210" cy="315" r="200" fill="none" stroke="{cfg['accent']}" stroke-width="0.7" opacity="0.12"/>
  <circle cx="210" cy="315" r="150" fill="none" stroke="{a3}" stroke-width="0.5" opacity="0.08" stroke-dasharray="4 8"/>
  <rect x="0" y="0" width="420" height="14" fill="rgba(0,0,0,0.5)"/>
  {"".join(f'<circle cx="{14+i*20}" cy="7" r="4" fill="{cfg["bg"][1]}" stroke="{cfg["accent"]}" stroke-width="1" opacity="0.5"/>' for i in range(21))}
  <rect x="0" y="616" width="420" height="14" fill="rgba(0,0,0,0.5)"/>
  {"".join(f'<circle cx="{14+i*20}" cy="623" r="4" fill="{cfg["bg"][1]}" stroke="{cfg["accent"]}" stroke-width="1" opacity="0.5"/>' for i in range(21))}
  <text x="210" y="155" text-anchor="middle" font-size="68" filter="url(#glw)" opacity="0.95">{cfg['icon']}</text>
  <rect x="150" y="167" width="120" height="22" rx="11" fill="{cfg['accent']}" opacity="0.75"/>
  <text x="210" y="182" text-anchor="middle" fill="#fff" font-size="10" font-weight="700" font-family="sans-serif" letter-spacing="3">{cfg['mood']}</text>
  {ts}{a_svg}{i_svg}{b_svg}{cs}
  <line x1="140" y1="{cy+62}" x2="280" y2="{cy+62}" stroke="{cfg['accent']}" stroke-width="1" opacity="0.25"/>
  <text x="210" y="{cy+88}" text-anchor="middle" fill="rgba(255,255,255,0.25)" font-size="11" font-family="sans-serif" letter-spacing="1">CINEBOOK - EXPERIENCE LIVE</text>
</svg>'''


# ── Poster Endpoint (must come before /{event_id}) ──

@router.get("/poster/{event_id}")
def get_event_poster(event_id: int):
    db = SessionLocal()
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return Response(content=_poster(event), media_type="image/svg+xml")
    finally:
        db.close()


# ── Event List / Detail ──

@router.get("", response_model=EventListOut)
def list_events(
    category: Optional[str] = Query(None, description="kids, music, comedy"),
    search: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Event)
    if category:
        query = query.filter(Event.category.ilike(f"%{category}%"))
    if search:
        like = f"%{search}%"
        query = query.filter(
            Event.title.ilike(like) | Event.artist_name.ilike(like)
            | Event.venue.ilike(like) | Event.description.ilike(like)
        )
    if city:
        query = query.filter(Event.city.ilike(f"%{city}%"))
    if language:
        query = query.filter(Event.language.ilike(f"%{language}%"))
    if min_price is not None:
        query = query.filter(Event.price >= min_price)
    if max_price is not None:
        query = query.filter(Event.price <= max_price)

    events = query.order_by(Event.trending.desc(), Event.event_date.asc()).all()
    all_cities = db.query(Event.city).distinct().all()
    cities = sorted({c[0] for c in all_cities if c[0]})

    return EventListOut(
        events=[EventOut.model_validate(e) for e in events],
        cities=cities,
    )


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventOut.model_validate(event)
