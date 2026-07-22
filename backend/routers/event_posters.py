from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import hashlib

from database import SessionLocal
from models import Event

router = APIRouter(prefix="/api/event-posters", tags=["Event Posters"])


KIDS_CONFIG = {
    "bg": ("#ff6b6b", "#ee5a24", "#ff6348"),
    "accent": "#ffd700",
    "text_accent": "#ffe066",
    "icon": "🧒",
    "mood": "KIDS ZONE",
    "gradient_angle": "135deg",
}

MUSIC_CONFIG = {
    "bg": ("#1a0533", "#4c1d95", "#2e1065"),
    "accent": "#c084fc",
    "text_accent": "#d8b4fe",
    "icon": "🎵",
    "mood": "LIVE MUSIC",
    "gradient_angle": "135deg",
}

COMEDY_CONFIG = {
    "bg": ("#451a03", "#b45309", "#78350f"),
    "accent": "#fbbf24",
    "text_accent": "#fde68a",
    "icon": "😂",
    "mood": "COMEDY NIGHT",
    "gradient_angle": "135deg",
}

CATEGORY_CONFIGS = {"kids": KIDS_CONFIG, "music": MUSIC_CONFIG, "comedy": COMEDY_CONFIG}


def _hash_color(seed, offset=0):
    h = int(hashlib.md5(seed.encode()).hexdigest()[:6], 16)
    r = ((h >> 16) & 0xFF + offset) % 256
    g = ((h >> 8) & 0xFF + offset) % 256
    b = ((h >> 0) & 0xFF + offset) % 256
    return f"#{r:02x}{g:02x}{b:02x}"


def _make_event_poster_svg(event):
    cfg = CATEGORY_CONFIGS.get(event.category, KIDS_CONFIG)
    title = event.title or "Untitled Event"
    artist = event.artist_name or ""
    venue = event.venue or ""
    city = event.city or ""
    event_date = ""
    if event.event_date:
        d = event.event_date
        months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                   "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        event_date = f"{d.day} {months[d.month - 1]} {d.year}"
    event_time = event.event_time or ""
    price = f"₹{int(event.price):,}" if event.price else ""
    rating = f"{event.rating:.1f}" if event.rating else ""
    language = event.language or ""
    age = event.age_recommendation or ""

    accent2 = _hash_color(title, 30)
    accent3 = _hash_color(title, -20)

    # Truncate title
    display = title if len(title) <= 26 else title[:23] + "..."
    lines = []
    if len(display) > 14:
        mid = display.rfind(" ", 0, len(display) // 2 + 5)
        if mid < 5:
            mid = len(display) // 2
        lines = [display[:mid].strip(), display[mid:].strip()]
    else:
        lines = [display]

    title_y_start = 210
    title_font = 28 if len(lines) == 1 else 24
    title_svg = ""
    for i, l in enumerate(lines):
        title_svg += f'<text x="210" y="{title_y_start + i * 36}" text-anchor="middle" fill="#fff" font-size="{title_font}" font-weight="900" font-family="Georgia, serif" letter-spacing="2" filter="url(#titleShadow)">{l}</text>\n'

    # Artist line
    artist_y = title_y_start + len(lines) * 36 + 18
    artist_svg = ""
    if artist:
        artist_svg = f'<text x="210" y="{artist_y}" text-anchor="middle" fill="{cfg["text_accent"]}" font-size="15" font-weight="600" font-family="sans-serif" letter-spacing="0.5" opacity="0.9">{artist}</text>\n'

    # Venue + Date
    info_y = artist_y + 28
    info_text = f"{venue}, {city}"
    if event_date:
        info_text = f"{event_date} • {event_time}" if event_time else event_date
    info_svg = f'<text x="210" y="{info_y}" text-anchor="middle" fill="rgba(255,255,255,0.65)" font-size="13" font-family="sans-serif" letter-spacing="0.5">{info_text}</text>\n'

    # Badges: Language, Age/Rating, Price
    badge_y = info_y + 38
    badges_svg = ""
    badge_items = []
    if language:
        badge_items.append(language)
    if age and event.category == "kids":
        badge_items.append(f"Ages {age}")
    elif rating:
        badge_items.append(f"★ {rating}")
    if price:
        badge_items.append(price)

    badge_width = 95
    total_badge_w = len(badge_items) * (badge_width + 35)
    start_x = 210 - total_badge_w // 2
    for i, item in enumerate(badge_items[:3]):
        bx = start_x + i * (badge_width + 35)
        badges_svg += (
            f'<rect x="{bx}" y="{badge_y}" width="{badge_width}" height="30" rx="15" fill="{cfg["accent"]}" opacity="0.15" stroke="{cfg["accent"]}" stroke-width="1" stroke-opacity="0.35"/>\n'
            f'<text x="{bx + badge_width/2}" y="{badge_y + 20}" text-anchor="middle" fill="{cfg["text_accent"]}" font-size="12" font-weight="700" font-family="sans-serif" letter-spacing="0.5">{item}</text>\n'
        )

    # Bottom CTA
    cta_y = badge_y + 60
    cta_svg = (
        f'<rect x="100" y="{cta_y}" width="220" height="48" rx="24" fill="url(#accentGrad)" filter="url(#softGlow)"/>\n'
        f'<text x="210" y="{cta_y + 32}" text-anchor="middle" fill="#fff" font-size="17" font-weight="800" font-family="sans-serif" letter-spacing="2">BOOK NOW ▸</text>\n'
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="630" viewBox="0 0 420 630">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{cfg['bg'][0]}"/>
      <stop offset="50%" stop-color="{cfg['bg'][1]}"/>
      <stop offset="100%" stop-color="{cfg['bg'][2]}"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{cfg['accent']}"/>
      <stop offset="100%" stop-color="{accent2}"/>
    </linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="titleShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-color="#000" flood-opacity="0.8"/>
    </filter>
    <filter id="softGlow">
      <feGaussianBlur stdDeviation="2" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="8" cy="8" r="1" fill="rgba(255,255,255,0.06)"/>
    </pattern>
  </defs>
  <rect width="420" height="630" fill="url(#bgGrad)"/>
  <rect width="420" height="630" fill="url(#dots)"/>
  <circle cx="380" cy="80" r="120" fill="{cfg['accent']}" opacity="0.06"/>
  <circle cx="40" cy="520" r="140" fill="{cfg['accent']}" opacity="0.06"/>
  <circle cx="210" cy="315" r="200" fill="none" stroke="{cfg['accent']}" stroke-width="0.7" opacity="0.12"/>
  <circle cx="210" cy="315" r="150" fill="none" stroke="{accent3}" stroke-width="0.5" opacity="0.08" stroke-dasharray="4 8"/>

  <!-- Film strip top -->
  <rect x="0" y="0" width="420" height="14" fill="rgba(0,0,0,0.5)"/>
  {"".join(f'<circle cx="{14+i*20}" cy="7" r="4" fill="{cfg["bg"][1]}" stroke="{cfg["accent"]}" stroke-width="1" opacity="0.5"/>' for i in range(21))}

  <!-- Film strip bottom -->
  <rect x="0" y="616" width="420" height="14" fill="rgba(0,0,0,0.5)"/>
  {"".join(f'<circle cx="{14+i*20}" cy="623" r="4" fill="{cfg["bg"][1]}" stroke="{cfg["accent"]}" stroke-width="1" opacity="0.5"/>' for i in range(21))}

  <!-- Category Icon -->
  <text x="210" y="155" text-anchor="middle" font-size="68" filter="url(#glow)" opacity="0.95">{cfg['icon']}</text>
  <rect x="150" y="167" width="120" height="22" rx="11" fill="{cfg['accent']}" opacity="0.75"/>
  <text x="210" y="182" text-anchor="middle" fill="#fff" font-size="10" font-weight="700" font-family="sans-serif" letter-spacing="3">{cfg['mood']}</text>

  {title_svg}
  {artist_svg}
  {info_svg}
  {badges_svg}
  {cta_svg}

  <line x1="140" y1="{cta_y + 62}" x2="280" y2="{cta_y + 62}" stroke="{cfg['accent']}" stroke-width="1" opacity="0.25"/>
  <text x="210" y="{cta_y + 88}" text-anchor="middle" fill="rgba(255,255,255,0.25)" font-size="11" font-family="sans-serif" letter-spacing="1">CINEBOOK • EXPERIENCE LIVE</text>
</svg>'''
    return svg


@router.get("/{event_id}")
def get_event_poster(event_id: int):
    db = SessionLocal()
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        # Always generate a stunning SVG poster for events
        svg = _make_event_poster_svg(event)
        return Response(content=svg, media_type="image/svg+xml")
    finally:
        db.close()
