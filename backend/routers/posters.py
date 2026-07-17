from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import httpx
import hashlib

from database import SessionLocal
from models import Movie
from omdb_client import search_poster_url

router = APIRouter(prefix="/api/posters", tags=["Posters"])

GENRE_PALETTES = {
    "Action": {"bg": ("#0d0614", "#1a0533", "#2d0a5c"), "accent": "#e63946", "text_accent": "#ff6b6b", "icon": "💥", "mood": "EXPLOSIVE"},
    "Romance": {"bg": ("#140610", "#330a22", "#5c1040"), "accent": "#ff6b9d", "text_accent": "#ff8fb3", "icon": "💕", "mood": "ROMANTIC"},
    "Thriller": {"bg": ("#060d14", "#0a1a33", "#0f2a5c"), "accent": "#00b4d8", "text_accent": "#48cae4", "icon": "🔍", "mood": "SUSPENSEFUL"},
    "Horror": {"bg": ("#0a0606", "#1a0a0a", "#331010"), "accent": "#9d0208", "text_accent": "#dc2f02", "icon": "👻", "mood": "TERRIFYING"},
}


def _genre_palette(genre, category):
    for key in GENRE_PALETTES:
        if key.lower() in (genre or "").lower() or key.lower() in (category or "").lower():
            return GENRE_PALETTES[key]
    return {"bg": ("#060610", "#0f0f25", "#181840"), "accent": "#f4a261", "text_accent": "#f4a261", "icon": "🎬", "mood": "MUST WATCH"}


def _hash_color(seed, offset=0):
    h = int(hashlib.md5(seed.encode()).hexdigest()[:6], 16)
    r = ((h >> 16) & 0xFF + offset) % 256
    g = ((h >> 8) & 0xFF + offset) % 256
    b = ((h >> 0) & 0xFF + offset) % 256
    return f"#{r:02x}{g:02x}{b:02x}"


def _make_poster_svg(movie):
    pal = _genre_palette(movie.genre, movie.category)
    title = movie.title
    year = str(movie.release_year) if movie.release_year else "—"
    imdb = f"{movie.imdb_rating:.1f}" if movie.imdb_rating else ""
    lang = movie.language or "—"
    genre = movie.genre or "—"
    h = movie.duration_min // 60 if movie.duration_min else 0
    m = movie.duration_min % 60 if movie.duration_min else 0
    duration = f"{h}h {m}m" if movie.duration_min else "—"
    accent2 = _hash_color(title, 30)

    display = title if len(title) <= 24 else title[:21] + "..."
    lines = []
    if len(display) > 13:
        mid = display.rfind(" ", 0, len(display) // 2 + 5)
        if mid < 5: mid = len(display) // 2
        lines = [display[:mid].strip(), display[mid:].strip()]
    else:
        lines = [display]

    title_y_start = 210
    title_font = 28 if len(lines) == 1 else 24
    title_svg = ""
    for i, l in enumerate(lines):
        title_svg += f'<text x="210" y="{title_y_start + i * 36}" text-anchor="middle" fill="#fff" font-size="{title_font}" font-weight="900" font-family="Georgia, serif" letter-spacing="2" filter="url(#titleShadow)">{l}</text>\n'

    star_y = title_y_start + len(lines) * 36 + 20
    star_svg = ""
    if imdb:
        star_svg = f'<rect x="160" y="{star_y - 22}" width="100" height="32" rx="16" fill="{pal["accent"]}" filter="url(#glow)"/>\n<text x="210" y="{star_y}" text-anchor="middle" fill="#fff" font-size="18" font-weight="800" font-family="sans-serif">★ {imdb}/10</text>\n'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="630" viewBox="0 0 420 630">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{pal['bg'][0]}"/>
      <stop offset="50%" stop-color="{pal['bg'][1]}"/>
      <stop offset="100%" stop-color="{pal['bg'][2]}"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{pal['accent']}"/>
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
  <circle cx="380" cy="80" r="120" fill="{pal['accent']}" opacity="0.04"/>
  <circle cx="40" cy="520" r="140" fill="{pal['accent']}" opacity="0.04"/>
  <circle cx="210" cy="315" r="200" fill="none" stroke="{pal['accent']}" stroke-width="0.5" opacity="0.1"/>
  <rect x="0" y="0" width="420" height="14" fill="rgba(0,0,0,0.5)"/>
  {"".join(f'<circle cx="{14+i*20}" cy="7" r="4" fill="{pal["bg"][2]}" stroke="{pal["accent"]}" stroke-width="1" opacity="0.5"/>' for i in range(21))}
  <rect x="0" y="616" width="420" height="14" fill="rgba(0,0,0,0.5)"/>
  {"".join(f'<circle cx="{14+i*20}" cy="623" r="4" fill="{pal["bg"][2]}" stroke="{pal["accent"]}" stroke-width="1" opacity="0.5"/>' for i in range(21))}
  <text x="210" y="165" text-anchor="middle" font-size="64" filter="url(#glow)" opacity="0.9">{pal['icon']}</text>
  <rect x="150" y="175" width="120" height="22" rx="11" fill="{pal['accent']}" opacity="0.7"/>
  <text x="210" y="190" text-anchor="middle" fill="#fff" font-size="10" font-weight="700" font-family="sans-serif" letter-spacing="3">{pal['mood']}</text>
  {title_svg}
  {star_svg}
  <rect x="30" y="425" width="110" height="34" rx="17" fill="{pal['accent']}" opacity="0.15" stroke="{pal['accent']}" stroke-width="1" stroke-opacity="0.3"/>
  <text x="85" y="446" text-anchor="middle" fill="{pal['text_accent']}" font-size="13" font-weight="700" font-family="sans-serif" letter-spacing="1">{lang}</text>
  <rect x="155" y="425" width="110" height="34" rx="17" fill="{pal['accent']}" opacity="0.15" stroke="{pal['accent']}" stroke-width="1" stroke-opacity="0.3"/>
  <text x="210" y="446" text-anchor="middle" fill="{pal['text_accent']}" font-size="13" font-weight="700" font-family="sans-serif" letter-spacing="1">{genre}</text>
  <rect x="280" y="425" width="110" height="34" rx="17" fill="{pal['accent']}" opacity="0.15" stroke="{pal['accent']}" stroke-width="1" stroke-opacity="0.3"/>
  <text x="335" y="446" text-anchor="middle" fill="{pal['text_accent']}" font-size="13" font-weight="700" font-family="sans-serif" letter-spacing="1">⭐ {imdb}</text>
  <text x="210" y="488" text-anchor="middle" fill="rgba(255,255,255,0.5)" font-size="14" font-family="sans-serif" letter-spacing="1">{duration}  •  {year}</text>
  <rect x="100" y="520" width="220" height="48" rx="24" fill="url(#accentGrad)" filter="url(#softGlow)"/>
  <text x="210" y="550" text-anchor="middle" fill="#fff" font-size="17" font-weight="800" font-family="sans-serif" letter-spacing="2">BOOK NOW ▸</text>
  <line x1="140" y1="572" x2="280" y2="572" stroke="{pal['accent']}" stroke-width="1" opacity="0.3"/>
  <text x="210" y="600" text-anchor="middle" fill="rgba(255,255,255,0.25)" font-size="11" font-family="sans-serif" letter-spacing="1">CINEBOOK • IN THEATRES NOW</text>
</svg>'''


async def _proxy_image(url: str) -> Response | None:
    """Download an image from url and return as Response, or None on failure."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=15, follow_redirects=True)
            if resp.status_code == 200 and len(resp.content) > 1000:
                ct = resp.headers.get("content-type", "image/jpeg")
                return Response(content=resp.content, media_type=ct)
    except Exception:
        pass
    return None


@router.get("/{movie_id}")
async def get_poster(movie_id: int):
    db = SessionLocal()
    try:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        # Tier 1: Try TMDB CDN poster_url from DB
        if movie.poster_url:
            result = await _proxy_image(movie.poster_url)
            if result:
                return result

        # Tier 2: Try OMDb API to find a poster
        omdb_url = await search_poster_url(movie.title, movie.release_year)
        if omdb_url:
            result = await _proxy_image(omdb_url)
            if result:
                return result

        # Tier 3: Generate cinema-grade SVG poster
        svg = _make_poster_svg(movie)
        return Response(content=svg, media_type="image/svg+xml")
    finally:
        db.close()
