"""
OMDb client — fetch movie poster URLs and proxy images.
OMDb is accessible on this network while TMDB API is blocked.
"""
import httpx
import urllib.parse

OMDB_API_KEY = "5eec5adc"
OMDB_BASE = "http://www.omdbapi.com/"

# In-memory cache: title|year|lang -> poster_url
_cache: dict[str, str | None] = {}


def _cache_key(title: str, year: int | None = None) -> str:
    return f"{title.strip().lower()}|{year or 0}"


async def search_poster_url(title: str, year: int | None = None) -> str | None:
    """Search OMDb for a movie and return the poster URL."""
    key = _cache_key(title, year)
    if key in _cache:
        return _cache[key]

    params = {"apikey": OMDB_API_KEY, "t": title, "type": "movie"}
    if year:
        params["y"] = str(year)

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(OMDB_BASE, params=params, timeout=10)
            if resp.status_code != 200:
                _cache[key] = None
                return None
            data = resp.json()
            if data.get("Response") == "True" and data.get("Poster") and data["Poster"] != "N/A":
                _cache[key] = data["Poster"]
                return data["Poster"]
    except Exception:
        pass

    # Fallback: search without year
    if year:
        try:
            params2 = {"apikey": OMDB_API_KEY, "s": title, "type": "movie"}
            async with httpx.AsyncClient() as client:
                resp = await client.get(OMDB_BASE, params=params2, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("Response") == "True":
                        for item in data.get("Search", []):
                            if str(item.get("Year", "")) == str(year):
                                # Fetch full details for poster
                                detail_resp = await client.get(
                                    OMDB_BASE,
                                    params={"apikey": OMDB_API_KEY, "i": item["imdbID"]},
                                    timeout=10,
                                )
                                if detail_resp.status_code == 200:
                                    detail = detail_resp.json()
                                    poster = detail.get("Poster")
                                    if poster and poster != "N/A":
                                        _cache[key] = poster
                                        return poster
        except Exception:
            pass

    _cache[key] = None
    return None
