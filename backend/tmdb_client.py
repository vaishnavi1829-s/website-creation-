"""
TMDB API client — search movies and retrieve poster URLs.
Uses the free TMDB API. Set TMDB_API_KEY env var for a custom key.
"""
import os
import httpx

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "2dca580c2a14b55200e784d157207b4d")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# In-memory cache: title|year -> poster_path
_cache: dict[str, str | None] = {}


def _cache_key(title: str, year: int | None = None) -> str:
    return f"{title.strip().lower()}|{year or 0}"


async def search_poster_path(title: str, year: int | None = None, language: str | None = None) -> str | None:
    """Search TMDB for a movie by title+year and return the poster_path (e.g. '/abc123.jpg')."""
    key = _cache_key(title, year)
    if key in _cache:
        return _cache[key]

    params: dict = {"api_key": TMDB_API_KEY, "query": title}
    if year:
        params["year"] = year
    if language and language.lower() == "tamil":
        params["language"] = "ta-IN"

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{TMDB_BASE_URL}/search/movie", params=params, timeout=10)
            if resp.status_code != 200:
                _cache[key] = None
                return None
            data = resp.json()
            results = data.get("results", [])

            # 1st pass: exact title match
            for r in results:
                candidates = [r.get("title", ""), r.get("original_title", "")]
                if any(c.strip().lower() == title.strip().lower() for c in candidates if c) and r.get("poster_path"):
                    _cache[key] = r["poster_path"]
                    return r["poster_path"]

            # 2nd pass: any result with a poster
            for r in results:
                if r.get("poster_path"):
                    _cache[key] = r["poster_path"]
                    return r["poster_path"]

            _cache[key] = None
            return None
    except Exception:
        _cache[key] = None
        return None


async def fetch_poster_image(poster_path: str) -> bytes | None:
    """Download the poster image bytes from TMDB's CDN."""
    url = f"{TMDB_IMAGE_BASE}{poster_path}"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=15)
            if resp.status_code == 200:
                return resp.content
            return None
    except Exception:
        return None
