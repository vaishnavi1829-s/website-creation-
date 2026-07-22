import { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import { fetchMovies, fetchNowShowingMovies, fetchShowtimes, fetchTheatres } from '../api';
import MovieCard from '../components/MovieCard';
import './Home.css';

const SECTION_ORDER = [
  { key: 'trending', label: '🔥 Trending Movies', filter: null, sort: (m) => m.trending, min: 1 },
  { key: 'tamil', label: '🎭 Tamil Movies', filter: { language: 'Tamil' } },
  { key: 'english', label: '🎬 English Movies', filter: { language: 'English' } },
  { key: 'romantic', label: '💕 Romantic', filter: { category: 'Romantic' } },
  { key: 'action', label: '💥 Action', filter: { category: 'Action' } },
  { key: 'thriller', label: '🔪 Thriller', filter: { category: 'Thriller' } },
  { key: 'horror', label: '👻 Horror/Ghost', filter: { category: 'Horror/Ghost' } },
];

export default function Home({ search, filters }) {
  const [allMovies, setAllMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [nowShowingMovies, setNowShowingMovies] = useState([]);
  const [nowShowingByTheatre, setNowShowingByTheatre] = useState([]);
  const [showtimesLoading, setShowtimesLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchMovies().then(data => { setAllMovies(data.movies || []); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  // Fetch now-showing data: theatres + showtimes grouped by theatre
  useEffect(() => {
    setShowtimesLoading(true);
    Promise.all([
      fetchTheatres(),
      fetchNowShowingMovies(7),
      fetchShowtimes(),
    ])
      .then(([theatres, nowMovies, showtimes]) => {
        setNowShowingMovies(nowMovies);
        // Build theatre -> movies -> showtimes mapping
        const movieMap = {};
        nowMovies.forEach(m => { movieMap[m.id] = m; });

        const theatreMap = {};
        theatres.forEach(t => {
          theatreMap[t.id] = { ...t, movies: [] };
        });

        const theatreMovieMap = {}; // theatre_id -> { movie_id -> { movie, showtimes[] } }
        showtimes.forEach(st => {
          const tid = null; // theatre_id not directly on showtime, we need the screen join
          // Actually showtimes returned from API have theatre_name etc. but not theatre_id.
          // We'll group by theatre_name instead.
          const key = st.theatre_name || 'Unknown';
          if (!theatreMovieMap[key]) {
            theatreMovieMap[key] = {
              name: key,
              location: st.theatre_location || '',
              facilities: st.theatre_facilities || '',
              movies: {},
            };
          }
          if (!theatreMovieMap[key].movies[st.movie_id]) {
            theatreMovieMap[key].movies[st.movie_id] = {
              movie: movieMap[st.movie_id],
              showtimes: [],
            };
          }
          if (theatreMovieMap[key].movies[st.movie_id]) {
            theatreMovieMap[key].movies[st.movie_id].showtimes.push(st);
          }
        });

        // Convert to array and sort showtimes; only include theatres with showtimes
        const grouped = Object.values(theatreMovieMap)
          .map(t => ({
            ...t,
            movies: Object.values(t.movies).filter(m => m.movie && m.showtimes.length > 0),
          }))
          .filter(t => t.movies.length > 0)
          .sort((a, b) => b.movies.length - a.movies.length);

        setNowShowingByTheatre(grouped);
        setShowtimesLoading(false);
      })
      .catch(() => setShowtimesLoading(false));
  }, []);

  // Carousel scroll state & refs
  const nowShowingScrollRef = useRef(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(false);

  const updateScrollButtons = useCallback(() => {
    const el = nowShowingScrollRef.current;
    if (!el) return;
    setCanScrollLeft(el.scrollLeft > 2);
    setCanScrollRight(el.scrollLeft < el.scrollWidth - el.clientWidth - 2);
  }, []);

  useEffect(() => {
    const el = nowShowingScrollRef.current;
    if (!el) return;
    updateScrollButtons();
    el.addEventListener('scroll', updateScrollButtons, { passive: true });
    window.addEventListener('resize', updateScrollButtons);
    return () => {
      el.removeEventListener('scroll', updateScrollButtons);
      window.removeEventListener('resize', updateScrollButtons);
    };
  }, [nowShowingByTheatre, updateScrollButtons]);

  const scroll = (direction) => {
    const el = nowShowingScrollRef.current;
    if (!el) return;
    const cardWidth = el.querySelector('.carousel-card')?.offsetWidth || 280;
    const scrollAmount = cardWidth * 2 + 16;
    el.scrollBy({ left: direction === 'left' ? -scrollAmount : scrollAmount, behavior: 'smooth' });
  };

  const handleWheel = useCallback((e) => {
    const el = nowShowingScrollRef.current;
    if (!el) return;
    e.preventDefault();
    el.scrollBy({ left: e.deltaY > 0 ? 300 : -300, behavior: 'smooth' });
  }, []);

  useEffect(() => {
    const el = nowShowingScrollRef.current;
    if (!el) return;
    el.addEventListener('wheel', handleWheel, { passive: false });
    return () => el.removeEventListener('wheel', handleWheel);
  }, [handleWheel]);

  const carouselMovies = useMemo(() => {
    const seen = new Set();
    const result = [];
    nowShowingByTheatre.forEach(theatre => {
      theatre.movies.forEach(({ movie, showtimes }) => {
        if (!seen.has(movie.id)) {
          seen.add(movie.id);
          result.push({ movie, theatre, showtimes });
        }
      });
    });
    return result;
  }, [nowShowingByTheatre]);

  // Filter based on search + active filters
  const filteredMovies = useMemo(() => {
    let list = allMovies;
    if (search) {
      const s = search.toLowerCase();
      list = list.filter(m => m.title.toLowerCase().includes(s));
    }
    if (filters.genre) list = list.filter(m => m.genre === filters.genre);
    if (filters.language) list = list.filter(m => m.language === filters.language);
    if (filters.rating) list = list.filter(m => m.rating === filters.rating);
    if (filters.release_year) list = list.filter(m => m.release_year === filters.release_year);
    return list;
  }, [allMovies, search, filters]);

  // Extract unique genres and languages for filters
  const genres = useMemo(() => [...new Set(allMovies.map(m => m.genre).filter(Boolean))].sort(), [allMovies]);
  const languages = useMemo(() => [...new Set(allMovies.map(m => m.language).filter(Boolean))].sort(), [allMovies]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner" />
        <p>Loading movies...</p>
      </div>
    );
  }

  const hasFilters = search || filters.genre || filters.language || filters.rating || filters.release_year;

  // Filtered view
  if (hasFilters) {
    return (
      <div className="home-page">
        <div className="section-container">
          <h2 className="section-title">Search Results ({filteredMovies.length})</h2>
          {filteredMovies.length === 0 ? (
            <div className="empty-state">
              <p>No movies found matching your criteria.</p>
              <p>Try adjusting your search or filters.</p>
            </div>
          ) : (
            <div className="movies-grid">{filteredMovies.map(m => <MovieCard key={m.id} movie={m} />)}</div>
          )}
        </div>
      </div>
    );
  }

  const formatShowtime = (iso) => {
    const d = new Date(iso);
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
  };

  const formatDate = (iso) => {
    const d = new Date(iso);
    return d.toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short' });
  };

  return (
    <div className="home-page">
      {/* Hero banner */}
      <div className="hero-banner">
        <div className="hero-content animate-fade-in">
          <h1>Experience Cinema Like Never Before</h1>
          <p>Book your tickets for the latest blockbusters. Tamil & English movies in IMAX, Dolby & Standard screens.</p>
        </div>
        <div className="hero-overlay" />
      </div>

      {/* Now Showing – Horizontal Carousel */}
      {!showtimesLoading && carouselMovies.length > 0 && (
        <div className="now-showing-section section-container animate-fade-in-up">
          <div className="carousel-header">
            <h2 className="section-title">🎬 Now Showing in Theatres</h2>
            <div className="carousel-arrows">
              <button
                className={`carousel-arrow carousel-arrow-left ${!canScrollLeft ? 'carousel-arrow--hidden' : ''}`}
                onClick={() => scroll('left')}
                aria-label="Scroll left"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
              </button>
              <button
                className={`carousel-arrow carousel-arrow-right ${!canScrollRight ? 'carousel-arrow--hidden' : ''}`}
                onClick={() => scroll('right')}
                aria-label="Scroll right"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
              </button>
            </div>
          </div>
          <div className="carousel-track" ref={nowShowingScrollRef}>
            {carouselMovies.map(({ movie, theatre, showtimes }) => {
              const hours = Math.floor((movie.duration_min || 0) / 60);
              const mins = (movie.duration_min || 0) % 60;
              const duration = hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
              return (
                <div key={movie.id} className="carousel-card">
                  {/* Poster */}
                  <div className="carousel-card-poster" onClick={() => window.location.href = `/movie/${movie.id}`}>
                    <img
                      src={`/api/posters/${movie.id}`}
                      alt={movie.title}
                      loading="lazy"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextElementSibling.style.display = 'flex';
                      }}
                    />
                    <div className="carousel-no-poster" style={{ display: 'none' }}>
                      <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect width="48" height="48" rx="6" fill="#1a1a2e" stroke="#3a3a55" strokeWidth="1.5" />
                        <path d="M16 32V16l10 8-10 8z" fill="#6b6b80" />
                        <rect x="28" y="16" width="8" height="16" rx="1" fill="#6b6b80" />
                      </svg>
                      <span>No Poster</span>
                    </div>
                    {/* IMDB Badge */}
                    {movie.imdb_rating && (
                      <div className="carousel-imdb-badge">
                        <span>★</span>{movie.imdb_rating}
                      </div>
                    )}
                    {/* Certification Badge */}
                    {movie.rating && (
                      <div className="carousel-cert-badge">{movie.rating}</div>
                    )}
                    {/* Hover overlay */}
                    <div className="carousel-card-overlay">
                      <span className="carousel-watch-btn">▶ Watch Now</span>
                    </div>
                  </div>
                  {/* Info */}
                  <div className="carousel-card-info">
                    <h3
                      className="carousel-card-title"
                      onClick={() => window.location.href = `/movie/${movie.id}`}
                    >
                      {movie.title}
                    </h3>
                    <div className="carousel-card-meta">
                      {movie.genre && <span className="carousel-meta-tag carousel-genre-tag">{movie.genre}</span>}
                      {movie.language && <span className="carousel-meta-tag carousel-lang-tag">{movie.language}</span>}
                      {movie.rating && <span className="carousel-meta-tag carousel-cert-tag">{movie.rating}</span>}
                    </div>
                    <div className="carousel-card-details">
                      {movie.duration_min > 0 && <span>{duration}</span>}
                      {movie.duration_min > 0 && movie.imdb_rating && <span className="carousel-dot">•</span>}
                      {movie.imdb_rating && <span className="carousel-imdb-text">★ {movie.imdb_rating}</span>}
                    </div>
                    <div className="carousel-card-theatre">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
                      <span>{theatre.name}</span>
                    </div>
                    {/* Showtime chips */}
                    {showtimes.length > 0 && (
                      <div className="carousel-showtimes">
                        {showtimes.slice(0, 4).map(st => (
                          <button
                            key={st.id}
                            className="carousel-time-chip"
                            onClick={() => window.location.href = `/book/${movie.id}`}
                          >
                            {formatShowtime(st.start_time)}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {SECTION_ORDER.map(section => {
        let sectionMovies;
        if (section.key === 'trending') {
          sectionMovies = filteredMovies.filter(m => m.trending > 0).sort((a, b) => b.trending - a.trending).slice(0, 6);
        } else if (section.filter) {
          sectionMovies = filteredMovies.filter(m => {
            return Object.entries(section.filter).every(([k, v]) => m[k] === v);
          });
        }
        if (!sectionMovies || sectionMovies.length === 0) return null;
        return (
          <div key={section.key} className="section-container animate-fade-in-up">
            <h2 className="section-title">{section.label}</h2>
            <div className="movies-grid">{sectionMovies.map(m => <MovieCard key={m.id} movie={m} />)}</div>
          </div>
        );
      })}
    </div>
  );
}
